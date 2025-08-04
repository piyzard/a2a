"""Multi-cluster create function for KubeStellar."""

import asyncio
from typing import Any, Dict, List, Optional

from ..base_functions import BaseFunction


class MultiClusterCreateFunction(BaseFunction):
    """Function to create resources across multiple Kubernetes clusters."""
    
    def __init__(self):
        super().__init__(
            name="multicluster_create",
            description="Create Kubernetes resources across multiple clusters in a KubeStellar environment"
        )
    
    async def execute(
        self, 
        resource_type: str = "",
        resource_name: str = "",
        filename: str = "",
        image: str = "",
        replicas: int = 1,
        port: int = 0,
        namespace: str = "",
        kubeconfig: str = "",
        remote_context: str = "",
        dry_run: str = "none",
        labels: Dict[str, str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Create resources across multiple Kubernetes clusters.
        
        Args:
            resource_type: Type of resource to create (deployment, service, etc.)
            resource_name: Name of the resource
            filename: Path to YAML/JSON file to create from
            image: Container image for deployments
            replicas: Number of replicas for deployments
            port: Port to expose for deployments
            namespace: Target namespace
            kubeconfig: Path to kubeconfig file
            remote_context: Remote context for cluster discovery
            dry_run: Dry run mode (none, client, server)
            labels: Labels to apply to resources
        
        Returns:
            Dictionary with creation results from all clusters
        """
        try:
            # Validate inputs
            if not filename and not resource_type:
                return {
                    "status": "error",
                    "error": "Either filename or resource_type must be specified"
                }
            
            if resource_type and not resource_name:
                return {
                    "status": "error", 
                    "error": "resource_name is required when resource_type is specified"
                }
            
            # Discover clusters
            clusters = await self._discover_clusters(kubeconfig, remote_context)
            if not clusters:
                return {
                    "status": "error",
                    "error": "No clusters discovered"
                }
            
            # Show binding policy recommendation for resource creation
            if resource_type and not filename:
                warning_msg = (
                    "WARNING: Direct resource creation across multiple clusters is not recommended. "
                    "Consider using KubeStellar binding policies for better multi-cluster management."
                )
            
            # Execute create command on all clusters
            results = {}
            for cluster in clusters:
                cluster_result = await self._create_on_cluster(
                    cluster, resource_type, resource_name, filename, image, 
                    replicas, port, namespace, kubeconfig, dry_run, labels
                )
                results[cluster["name"]] = cluster_result
            
            success_count = sum(1 for r in results.values() if r["status"] == "success")
            total_count = len(results)
            
            return {
                "status": "success" if success_count > 0 else "error",
                "clusters_total": total_count,
                "clusters_succeeded": success_count,
                "clusters_failed": total_count - success_count,
                "results": results,
                "warning": warning_msg if resource_type and not filename else None
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to create resources: {str(e)}"
            }
    
    async def _discover_clusters(self, kubeconfig: str, remote_context: str) -> List[Dict[str, Any]]:
        """Discover available clusters using kubectl."""
        try:
            clusters = []
            
            # Get kubeconfig contexts
            cmd = ["kubectl", "config", "get-contexts", "-o", "name"]
            if kubeconfig:
                cmd.extend(["--kubeconfig", kubeconfig])
            
            result = await self._run_command(cmd)
            if result["returncode"] != 0:
                return []
            
            contexts = result["stdout"].strip().split("\n")
            
            # Test connectivity to each context
            for context in contexts:
                if not context.strip():
                    continue
                    
                # Skip WDS (Workload Description Space) clusters
                if self._is_wds_cluster(context):
                    continue
                
                # Test cluster connectivity
                test_cmd = ["kubectl", "cluster-info", "--context", context]
                if kubeconfig:
                    test_cmd.extend(["--kubeconfig", kubeconfig])
                
                test_result = await self._run_command(test_cmd)
                if test_result["returncode"] == 0:
                    clusters.append({
                        "name": context,
                        "context": context,
                        "status": "Ready"
                    })
            
            return clusters
            
        except Exception:
            return []
    
    def _is_wds_cluster(self, cluster_name: str) -> bool:
        """Check if cluster is a WDS (Workload Description Space) cluster."""
        lower_name = cluster_name.lower()
        return (
            lower_name.startswith("wds") or 
            "-wds-" in lower_name or 
            "_wds_" in lower_name
        )
    
    async def _create_on_cluster(
        self, 
        cluster: Dict[str, Any], 
        resource_type: str,
        resource_name: str,
        filename: str,
        image: str,
        replicas: int,
        port: int,
        namespace: str,
        kubeconfig: str,
        dry_run: str,
        labels: Optional[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Create resource on a specific cluster."""
        try:
            # Build kubectl command
            cmd = ["kubectl"]
            
            if filename:
                cmd.extend(["apply", "-f", filename])
            else:
                cmd.extend(["create", resource_type, resource_name])
                
                # Add resource-specific parameters
                if resource_type == "deployment" and image:
                    cmd.extend(["--image", image])
                    if replicas > 1:
                        cmd.extend(["--replicas", str(replicas)])
                    if port > 0:
                        cmd.extend(["--port", str(port)])
            
            # Add common parameters
            cmd.extend(["--context", cluster["context"]])
            
            if kubeconfig:
                cmd.extend(["--kubeconfig", kubeconfig])
            
            if namespace:
                cmd.extend(["--namespace", namespace])
            
            if dry_run != "none":
                cmd.extend(["--dry-run", dry_run])
            
            # Execute command
            result = await self._run_command(cmd)
            
            if result["returncode"] == 0:
                return {
                    "status": "success",
                    "output": result["stdout"],
                    "cluster": cluster["name"]
                }
            else:
                # Provide friendly error messages
                error_output = result["stderr"] or result["stdout"]
                if "already exists" in error_output:
                    error_msg = "Resource already exists in this cluster"
                elif "not found" in error_output:
                    error_msg = "Resource or cluster not accessible"
                else:
                    error_msg = f"Creation failed: {error_output}"
                
                return {
                    "status": "error",
                    "error": error_msg,
                    "output": error_output,
                    "cluster": cluster["name"]
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to create on cluster {cluster['name']}: {str(e)}",
                "cluster": cluster["name"]
            }
    
    async def _run_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run a shell command asynchronously."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "returncode": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode()
            }
        except Exception as e:
            return {
                "returncode": 1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Define the JSON schema for function parameters."""
        return {
            "type": "object",
            "properties": {
                "resource_type": {
                    "type": "string",
                    "description": "Type of Kubernetes resource to create (deployment, service, configmap, secret, namespace)",
                    "enum": ["deployment", "service", "configmap", "secret", "namespace"]
                },
                "resource_name": {
                    "type": "string",
                    "description": "Name of the resource to create"
                },
                "filename": {
                    "type": "string",
                    "description": "Path to YAML/JSON file containing resource definitions"
                },
                "image": {
                    "type": "string",
                    "description": "Container image for deployments"
                },
                "replicas": {
                    "type": "integer",
                    "description": "Number of replicas for deployments",
                    "default": 1,
                    "minimum": 1
                },
                "port": {
                    "type": "integer",
                    "description": "Port to expose for deployments",
                    "default": 0,
                    "minimum": 0
                },
                "namespace": {
                    "type": "string",
                    "description": "Target namespace for resource creation"
                },
                "kubeconfig": {
                    "type": "string",
                    "description": "Path to kubeconfig file"
                },
                "remote_context": {
                    "type": "string",
                    "description": "Remote context for KubeStellar cluster discovery"
                },
                "dry_run": {
                    "type": "string",
                    "description": "Dry run mode",
                    "enum": ["none", "client", "server"],
                    "default": "none"
                },
                "labels": {
                    "type": "object",
                    "description": "Labels to apply to the created resources",
                    "additionalProperties": {"type": "string"}
                }
            },
            "anyOf": [
                {"required": ["filename"]},
                {"required": ["resource_type", "resource_name"]}
            ]
        }