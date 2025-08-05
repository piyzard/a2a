---
sidebar_position: 3
---

# Quick Start Guide

Get KubeStellar A2A up and running in 5 minutes! This guide will walk you through the essential steps to start managing your Kubernetes clusters with AI-powered automation.

## Prerequisites Check

Before we begin, make sure you have:
- ✅ Python 3.11+ installed
- ✅ kubectl configured with at least one cluster
- ✅ Internet connection for package downloads

## Step 1: Install KubeStellar A2A

Choose your preferred installation method:

### Using uv (Recommended)
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/kubestellar/a2a.git
cd a2a
uv pip install -e .
```

### Using pip
```bash
git clone https://github.com/kubestellar/a2a.git
cd a2a
pip install -e .
```

## Step 2: Verify Installation

Test that everything is working:

```bash
# Check installation
uv run kubestellar --help

# List available functions
uv run kubestellar list-functions
```

You should see output similar to:
```
Available functions:

- kubestellar_management
- get_kubeconfig
- helm_deploy
- multicluster_create
- gvrc_discovery
- namespace_utils
[... and more]
```

## Step 3: Basic Cluster Information

Let's start with something simple - get information about your Kubernetes clusters:

```bash
# Get basic cluster info
uv run kubestellar execute get_kubeconfig

# Get detailed cluster information
uv run kubestellar execute get_kubeconfig -P detail_level=full
```

Example output:
```json
{
  "status": "success",
  "current_context": "kind-kubestellar",
  "total_contexts": 3,
  "clusters": [
    {
      "name": "kind-kubestellar",
      "server": "https://127.0.0.1:45243",
      "status": "accessible"
    }
  ]
}
```

## Step 4: Explore Your Clusters

Discover what resources are available across your clusters:

```bash
# Discover all available Kubernetes resources
uv run kubestellar execute gvrc_discovery

# List namespaces across all clusters
uv run kubestellar execute namespace_utils -P operation=list -P all_namespaces=true
```

## Step 5: Try Multi-Cluster Operations

Create a simple resource across multiple clusters:

```bash
# Create a ConfigMap across all accessible clusters
uv run kubestellar execute multicluster_create \
  -P resource_type=configmap \
  -P resource_name=hello-a2a \
  -P data='{"message": "Hello from KubeStellar A2A!"}' \
  -P dry_run=true
```

The `dry_run=true` flag shows what would be created without actually creating it.

## Step 6: Advanced Features (Optional)

### KubeStellar Management
If you have KubeStellar installed:

```bash
# Get comprehensive KubeStellar topology
uv run kubestellar execute kubestellar_management -P operation=topology_map

# Perform deep search with binding policy analysis
uv run kubestellar execute kubestellar_management \
  -P operation=deep_search \
  -P binding_policies=true
```

### Helm Deployments
Deploy a simple application using Helm:

```bash
# Deploy nginx with KubeStellar binding policies
uv run kubestellar execute helm_deploy \
  -P chart_name=nginx \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P create_binding_policy=true \
  -P dry_run=true
```

## Step 7: Try the AI Agent (Optional)

Experience natural language Kubernetes management:

```bash
# Set up OpenAI API key (if you have one)
export OPENAI_API_KEY="your-api-key-here"

# Start the interactive agent
uv run kubestellar agent
```

In the agent, try natural language commands:
```
[openai] ▶ show me all my clusters
[openai] ▶ how many pods are running?
[openai] ▶ list all namespaces
```

## What You Just Did

🎉 **Congratulations!** You've successfully:

- ✅ Installed KubeStellar A2A
- ✅ Connected to your Kubernetes clusters
- ✅ Explored available resources and namespaces
- ✅ Performed multi-cluster operations
- ✅ Tested advanced features like KubeStellar integration and AI automation

## Next Steps

Now that you have KubeStellar A2A running, explore more advanced features:

### 📚 **Learn More**
- **[GitHub Repository →](https://github.com/kubestellar/a2a)** - Source code and comprehensive README
- **[Issues & Support →](https://github.com/kubestellar/a2a/issues)** - Report bugs and get help
- **[KubeStellar Project →](https://kubestellar.io)** - Learn about the broader ecosystem

### 🔧 **Advanced Features**
- **[Troubleshooting Guide →](../troubleshooting)** - Resolve common issues
- **[Complete Documentation →](https://github.com/kubestellar/a2a/blob/main/README.md)** - Full feature reference

## Common First Tasks

Here are some common things you might want to do next:

### Deploy Your First Application
```bash
# Deploy a sample application with Helm
uv run kubestellar execute helm_deploy \
  -P chart_name=podinfo \
  -P repository_url=https://stefanprodan.github.io/podinfo \
  -P namespace=default \
  -P create_binding_policy=true
```

### Monitor Your Clusters
```bash
# Get logs from all pods in a namespace
uv run kubestellar execute multicluster_logs \
  -P target_namespaces='["default"]' \
  -P tail=50

# Check resource usage across clusters
uv run kubestellar execute namespace_utils \
  -P operation=list-resources \
  -P all_namespaces=true
```

### Set Up Automation
```bash
# Create a script for daily cluster health checks
cat > daily-check.sh << 'EOF'
#!/bin/bash
echo "=== Daily Kubernetes Cluster Health Check ==="
uv run kubestellar execute kubestellar_management -P operation=topology_map
uv run kubestellar execute namespace_utils -P operation=list -P all_namespaces=true
echo "=== Health check complete ==="
EOF

chmod +x daily-check.sh
./daily-check.sh
```

## Troubleshooting

### Installation Issues
```bash
# Verify Python version
python --version  # Should be 3.11+

# Check kubectl connectivity
kubectl cluster-info

# Verify installation
uv run kubestellar execute get_kubeconfig
```

### Common Errors

**"Function not found"**: Make sure you're using the correct function name from `list-functions`

**"Kubeconfig not found"**: Ensure kubectl is configured and `$KUBECONFIG` is set correctly

**"Permission denied"**: You might need cluster admin permissions for some operations

### Getting Help

- **Documentation**: You're reading it! 📖
- **GitHub Issues**: [Report bugs](https://github.com/kubestellar/a2a/issues)
- **Discussions**: [Ask questions](https://github.com/kubestellar/a2a/discussions)

---

*Ready to transform your Kubernetes management experience? Let's dive deeper! 🚀*