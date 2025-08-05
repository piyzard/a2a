# KubeStellar A2A Agent

A powerful, unified implementation of both MCP (Model Context Protocol) server and KubeStellar Agent CLI tool with shared functions for Kubernetes multi-cluster management and orchestration. Now featuring comprehensive multi-namespace support and GVRC (Group, Version, Resource, Category) discovery capabilities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [KubeStellar CLI](#kubestellar-cli)
  - [MCP Server](#mcp-server)
- [Available Functions](#available-functions)
- [Development](#development)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

KubeStellar is a comprehensive tool designed to simplify Kubernetes multi-cluster management through a dual-interface approach:

1. **CLI Interface**: Direct command-line access for developers and operators
2. **MCP Server**: Integration with AI assistants like Claude Desktop for intelligent cluster management

The tool provides a shared function architecture, ensuring consistency between both interfaces while enabling powerful automation and management capabilities.

## Features

- 🔄 **Dual Interface**: Use the same functions via CLI or through AI assistants
- 🌐 **Multi-Cluster Support**: Manage multiple Kubernetes clusters from a single interface
- ⚓ **Helm Integration**: Complete Helm chart deployment with KubeStellar binding policies ✨ **NEW**
- 🏷️ **Multi-Namespace Operations**: Full support for all-namespaces, namespace selectors, and targeted deployments
- 🔍 **GVRC Discovery**: Complete resource discovery including Groups, Versions, Resources, and Categories
- 🎯 **KubeStellar 2024**: Full support for WDS, ITS, WEC architecture and binding policies
- 🔧 **Extensible Architecture**: Easy to add new functions and capabilities
- 🔒 **Type-Safe**: Full type hints and schema validation for reliability
- 🚀 **Async Support**: Built with modern async/await patterns for performance
- 📝 **Rich Documentation**: Comprehensive guides for users and developers
- 🧪 **Well-Tested**: Includes comprehensive test suite with 60+ passing tests
- 📦 **uv Compatible**: Built and tested with the modern uv package manager

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interfaces                       │
├─────────────────────┬───────────────────────────────────────┤
│   KubeStellar CLI   │        MCP Server (Claude)            │
├─────────────────────┴───────────────────────────────────────┤
│                    Shared Function Layer                     │
├─────────────────────────────────────────────────────────────┤
│                    Function Registry                         │
├─────────────────────────────────────────────────────────────┤
│                 Individual Functions                         │
│  (kubeconfig, cluster management, deployments, etc.)        │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

- **Shared Functions**: Core business logic implemented once, used everywhere
- **Function Registry**: Dynamic registration system for function discovery
- **Base Function Class**: Abstract base providing consistent interface
- **Type System**: JSON Schema-based parameter validation

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- kubectl configured (for Kubernetes functions)

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/kubestellar.git
cd kubestellar

# Install with uv (includes all dependencies)
uv pip install -e ".[dev]"
```

**Note**: The project has been tested and verified with uv. All CLI commands are available through `uv run`.

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/kubestellar.git
cd kubestellar

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -e .
```

### Verify Installation

```bash
# Check CLI installation
uv run kubestellar --help

# List available functions
uv run kubestellar list-functions
```

**Note**: Since we're using uv for package management, all commands should be prefixed with `uv run` unless you've activated the virtual environment.

## Quick Start

### CLI Quick Start

```bash
# 1. List all available functions
uv run kubestellar list-functions

# 2. Get your current Kubernetes context
uv run kubestellar execute get_kubeconfig

# 3. Get detailed cluster information
uv run kubestellar execute get_kubeconfig --param detail_level=full

# 4. Get help for a specific function
uv run kubestellar describe get_kubeconfig

# 5. Discover resources across all clusters
uv run kubestellar execute gvrc_discovery

# 6. List all namespaces across clusters
uv run kubestellar execute namespace_utils -P all_namespaces=true
```

### MCP Server Quick Start

1. Add to Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kubestellar": {
      "command": "uv",
      "args": ["run", "kubestellar-mcp"],
      "cwd": "/path/to/a2a"
    }
  }
}
```

2. Restart Claude Desktop
3. Start using KubeStellar functions in your conversations

## Usage

### KubeStellar CLI

The CLI provides multiple interfaces for interacting with KubeStellar functions:

#### Main Commands

```bash
# List all available functions
uv run kubestellar list-functions

# Execute a function with parameters
uv run kubestellar execute <function_name> [parameters]

# Get detailed function description and schema
uv run kubestellar describe <function_name>

# Start interactive agent mode (NEW)
uv run kubestellar agent

# Show CLI help
uv run kubestellar --help
```

#### List Functions

```bash
uv run kubestellar list-functions
```

Output:
```
Available functions:

- kubestellar_management
  Description: Advanced KubeStellar multi-cluster resource management with deep search capabilities, binding policy integration, work status tracking, and comprehensive cluster topology analysis
  
- get_kubeconfig
  Description: Get details from kubeconfig file including contexts, clusters, and users
  
- helm_deploy (NEW)
  Description: Deploy Helm charts across clusters with KubeStellar binding policy integration. Supports chart repositories, local charts, cluster-specific values, and automatic resource labeling for BindingPolicy compatibility
  
- namespace_utils  
  Description: List and count pods, services, deployments and other resources across namespaces and clusters
  
- gvrc_discovery
  Description: Discover and inventory all available Kubernetes API resources across clusters
  
- multicluster_create
  Description: Create Kubernetes resources across multiple clusters with advanced namespace targeting
  
- multicluster_logs
  Description: Aggregate and stream logs from containers across multiple clusters and namespaces
  
- deploy_to
  Description: Deploy resources to specific clusters with advanced targeting and customization options
```

#### Execute Functions

**Basic execution:**
```bash
uv run kubestellar execute <function_name>
```

**With parameters (multiple syntax options):**
```bash
# Using --param flag
uv run kubestellar execute get_kubeconfig --param context=production --param detail_level=full

# Using -P shorthand (recommended)
uv run kubestellar execute get_kubeconfig -P context=staging -P detail_level=contexts

# Using JSON parameters
uv run kubestellar execute get_kubeconfig --params '{"context": "production", "detail_level": "full"}'

# Complex array parameters
uv run kubestellar execute namespace_utils -P target_namespaces='["prod","staging"]' -P all_namespaces=true
```

#### Describe Functions

```bash
uv run kubestellar describe <function_name>
```

Example output:
```
Function: kubestellar_management
Description: Advanced KubeStellar multi-cluster resource management with deep search capabilities, binding policy integration, work status tracking, and comprehensive cluster topology analysis

Schema:
{
  "type": "object", 
  "properties": {
    "operation": {
      "type": "string",
      "enum": ["deep_search", "policy_analysis", "resource_inventory", "topology_map"],
      "default": "deep_search"
    },
    "binding_policies": {
      "type": "boolean", 
      "description": "Include binding policy analysis",
      "default": true
    },
    "deep_analysis": {
      "type": "boolean",
      "description": "Perform deep dependency and relationship analysis", 
      "default": true
    }
  }
}
```

### Interactive Agent Mode (NEW)

The KubeStellar Agent provides an interactive AI-powered interface for natural language cluster management:

#### Starting the Agent

```bash
uv run kubestellar agent
```

This starts an interactive session with:
- **Natural language processing** for Kubernetes operations
- **Multi-cluster topology awareness**
- **KubeStellar 2024 architecture support**
- **Real-time resource analysis**
- **Binding policy integration**

#### Agent Interface

```
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│  ██╗  ██╗██╗   ██╗██████╗ ███████╗███████╗████████╗███████╗██╗     ██╗      █████╗ ██████╗  │
│  ██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██║     ██║     ██╔══██╗██╔══██╗ │
│  █████╔╝ ██║   ██║██████╔╝█████╗  ███████╗   ██║   █████╗  ██║     ██║     ███████║██████╔╝ │
│  ██╔═██╗ ██║   ██║██╔══██╗██╔══╝  ╚════██║   ██║   ██╔══╝  ██║     ██║     ██╔══██║██╔══██╗ │
│  ██║  ██╗╚██████╔╝██████╔╝███████╗███████║   ██║   ███████╗███████╗███████╗██║  ██║██║  ██║ │
│  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ │
│                       Multi-Cluster Kubernetes Management Agent                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯

Provider: openai
Model: gpt-4o

Type 'help' for available commands
Type 'exit' or Ctrl+D to quit

[openai] ▶ 
```

#### Agent Commands

**Natural language queries:**
```bash
# Resource analysis
[openai] ▶ how many pods are running?
[openai] ▶ show me kubestellar topology
[openai] ▶ perform deep kubestellar search with binding policies
[openai] ▶ analyze resource placement across clusters

# KubeStellar-specific operations  
[openai] ▶ show me all WDS and ITS spaces
[openai] ▶ check binding policy status
[openai] ▶ list workstatuses across clusters
[openai] ▶ analyze manifest works distribution

# Troubleshooting
[openai] ▶ check cluster connectivity
[openai] ▶ find failed deployments
[openai] ▶ show resource distribution issues
```

**Built-in commands:**
```bash
help          # Show available commands
clear         # Clear conversation history  
provider <name>  # Switch AI provider
exit          # Exit the agent
```

#### Agent Configuration

Configure AI providers in `~/.kube/a2a-config.yaml`:

```yaml
providers:
  openai:
    api_key: "your-openai-key"
    model: "gpt-4o"
    temperature: 0.7
  
  claude:
    api_key: "your-claude-key" 
    model: "claude-3-haiku"
    
default_provider: "openai"

ui:
  show_thinking: true
  show_token_usage: true
```

Or set environment variables:
```bash
export OPENAI_API_KEY="your-key"
export CLAUDE_API_KEY="your-key"  
export A2A_DEFAULT_PROVIDER="openai"
```

### MCP Server

The MCP server integrates seamlessly with Claude Desktop and other MCP-compatible clients.

#### Configuration Options

```json
{
  "mcpServers": {
    "kubestellar": {
      "command": "uv",
      "args": ["run", "kubestellar-mcp"],
      "cwd": "/path/to/kubestellar",
      "env": {
        "KUBECONFIG": "/custom/path/to/kubeconfig",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### Using with Claude

Once configured, you can interact naturally:

```
User: "Can you check my Kubernetes clusters?"
Claude: "I'll check your Kubernetes configuration for you."
[Uses get_kubeconfig function]

User: "Show me the production context details"
Claude: "Let me get the details for your production context."
[Uses get_kubeconfig with context parameter]
```

## Available Functions

The KubeStellar Agent provides comprehensive multi-cluster management functions with advanced namespace and resource discovery capabilities, enhanced with KubeStellar 2024 architecture support.

### KubeStellar Management Functions

#### kubestellar_management (NEW)

Advanced KubeStellar multi-cluster resource management with deep search capabilities, binding policy integration, work status tracking, and comprehensive cluster topology analysis.

**Key Features:**
- **KubeStellar 2024 Architecture**: Full support for WDS, ITS, WEC spaces
- **Binding Policy Analysis**: Analyze BindingPolicies, WorkStatuses, ManifestWorks
- **Deep Search**: Multi-cluster resource discovery with relationship mapping
- **Topology Mapping**: Visual representation of KubeStellar control plane
- **OCM Integration**: Support for Open Cluster Management components

**Parameters:**
- `operation` (string): Operation type (`deep_search`, `policy_analysis`, `resource_inventory`, `topology_map`)
- `binding_policies` (boolean): Include binding policy analysis (default: true)
- `work_statuses` (boolean): Include work status tracking (default: true)
- `placement_analysis` (boolean): Analyze resource placement strategies (default: true)
- `deep_analysis` (boolean): Perform deep dependency analysis (default: true)
- `include_wds` (boolean): Include WDS clusters in analysis (default: false)

**Examples:**

```bash
# KubeStellar topology overview
uv run kubestellar execute kubestellar_management -P operation=topology_map

# Deep search with binding policies
uv run kubestellar execute kubestellar_management -P operation=deep_search -P binding_policies=true

# Analyze binding policies across clusters
uv run kubestellar execute kubestellar_management -P operation=policy_analysis

# Resource inventory with placement analysis
uv run kubestellar execute kubestellar_management -P operation=resource_inventory -P placement_analysis=true

# Include WDS spaces in analysis
uv run kubestellar execute kubestellar_management -P include_wds=true -P deep_analysis=true
```

**Agent Mode Examples:**
```bash
# Start agent mode
uv run kubestellar agent

# Natural language KubeStellar queries
[openai] ▶ show me kubestellar topology
[openai] ▶ perform deep kubestellar search with binding policies  
[openai] ▶ analyze workstatus distribution across clusters
[openai] ▶ check manifest work synchronization
[openai] ▶ show me WDS and ITS spaces

# Helm deployment queries
[openai] ▶ deploy nginx using helm to production clusters
[openai] ▶ install prometheus helm chart with binding policy
[openai] ▶ upgrade my application helm release
```

### Helm Deployment Functions

#### helm_deploy (NEW)

Deploy Helm charts across multiple clusters with full KubeStellar binding policy integration and automatic resource labeling.

**Key Features:**
- **Multi-Source Support**: Deploy from Helm repositories, local charts, or packaged files
- **KubeStellar Integration**: Automatic BindingPolicy creation and resource labeling
- **Cluster Targeting**: Deploy to specific clusters or use label selectors
- **Advanced Configuration**: Per-cluster values files and set values
- **Full Lifecycle**: Install, upgrade, uninstall, status, and history operations
- **Namespace Management**: Create and label namespaces automatically

**Core Parameters:**
- `chart_name` (string): Name of the Helm chart (e.g., "nginx-ingress", "prometheus")
- `chart_version` (string, optional): Specific chart version to deploy
- `repository_url` (string, optional): Helm repository URL
- `repository_name` (string, optional): Local repository name
- `chart_path` (string, optional): Path to local chart directory or .tgz file
- `release_name` (string, optional): Helm release name (defaults to chart name)
- `operation` (string): Helm operation - "install", "upgrade", "uninstall", "status", "history" (default: "install")

**Targeting Parameters:**
- `target_clusters` (array): Names of specific clusters to deploy to
- `cluster_labels` (array): Label selectors for cluster targeting
- `namespace` (string): Target namespace (default: "default")
- `all_namespaces` (boolean): Deploy across all namespaces
- `target_namespaces` (array): Specific list of target namespaces

**Configuration Parameters:**
- `values_file` (string): Path to global values file
- `values_files` (array): List of values files to apply
- `cluster_values` (array): Per-cluster values files in "cluster=values.yaml" format
- `set_values` (array): Set values in "key=value" format
- `cluster_set_values` (array): Per-cluster set values in "cluster=key=value" format

**KubeStellar Parameters:**
- `create_binding_policy` (boolean): Create KubeStellar binding policy (default: true)
- `binding_policy_name` (string): Name for the binding policy
- `cluster_selector_labels` (object): Labels for cluster selection in binding policy
- `kubestellar_labels` (object): Additional KubeStellar labels for resources
- `wds_context` (string): WDS (Workload Description Space) context

**Operation Parameters:**
- `create_namespace` (boolean): Create namespace if it doesn't exist (default: true)
- `wait` (boolean): Wait for deployment to complete (default: true)
- `timeout` (string): Deployment timeout (default: "5m")
- `atomic` (boolean): Atomic deployment with rollback on failure
- `dry_run` (boolean): Show what would be deployed without doing it

**Basic Examples:**

```bash
# Deploy nginx-ingress from repository
uv run kubestellar execute helm_deploy \
  -P chart_name=ingress-nginx \
  -P repository_url=https://kubernetes.github.io/ingress-nginx \
  -P target_clusters='["cluster1","cluster2"]' \
  -P namespace=ingress-system

# Deploy from local chart with custom values
uv run kubestellar execute helm_deploy \
  -P chart_path=./charts/myapp \
  -P release_name=myapp-prod \
  -P values_file=values-prod.yaml \
  -P target_clusters='["prod-cluster"]'

# Deploy with per-cluster configuration
uv run kubestellar execute helm_deploy \
  -P chart_name=prometheus \
  -P repository_name=prometheus-community \
  -P cluster_values='["cluster1=values-cluster1.yaml","cluster2=values-cluster2.yaml"]' \
  -P set_values='["persistence.enabled=true"]' \
  -P cluster_set_values='["cluster1=storage.size=100Gi","cluster2=storage.size=50Gi"]'
```

**KubeStellar Integration Examples:**

```bash
# Deploy with custom binding policy
uv run kubestellar execute helm_deploy \
  -P chart_name=nginx \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P binding_policy_name=nginx-edge-policy \
  -P cluster_selector_labels='{"location-group":"edge","environment":"production"}' \
  -P wds_context=wds-cluster

# Deploy across all namespaces with binding policy
uv run kubestellar execute helm_deploy \
  -P chart_name=monitoring-stack \
  -P chart_path=./charts/monitoring \
  -P all_namespaces=true \
  -P kubestellar_labels='{"app-tier":"infrastructure","managed-by":"platform-team"}'

# Deploy with namespace selector and binding policy
uv run kubestellar execute helm_deploy \
  -P chart_name=logging-agent \
  -P repository_url=https://charts.fluentd.org \
  -P namespace_selector="environment in (prod,staging)" \
  -P cluster_selector_labels='{"node-type":"worker"}'
```

**Lifecycle Management Examples:**

```bash
# Upgrade existing release to new version
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=myapp \
  -P chart_version=2.0.0 \
  -P release_name=myapp-prod \
  -P repository_url=https://charts.mycompany.com \
  -P atomic=true

# Upgrade with new values file
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=nginx \
  -P release_name=nginx-prod \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P values_file=values-v2.yaml \
  -P set_values='["replicaCount=5","resources.limits.memory=1Gi"]' \
  -P wait=true \
  -P timeout=10m

# Upgrade with cluster-specific configurations
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=prometheus \
  -P chart_version=15.0.0 \
  -P release_name=monitoring \
  -P repository_name=prometheus-community \
  -P cluster_values='["prod-us=values-us-v2.yaml","prod-eu=values-eu-v2.yaml"]' \
  -P cluster_set_values='["prod-us=storage.size=200Gi","prod-eu=storage.size=150Gi"]' \
  -P target_clusters='["prod-us","prod-eu"]'

# Check release status across clusters
uv run kubestellar execute helm_deploy \
  -P operation=status \
  -P release_name=nginx-ingress \
  -P target_clusters='["cluster1","cluster2"]'

# View release history
uv run kubestellar execute helm_deploy \
  -P operation=history \
  -P release_name=prometheus \
  -P target_clusters='["monitoring-cluster"]'

# Rollback to previous version (using upgrade with revision)
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P release_name=myapp \
  -P chart_name=myapp \
  -P repository_url=https://charts.mycompany.com \
  -P set_values='["--set","rollback=true"]' \
  -P target_clusters='["prod-cluster"]'

# Uninstall release from specific clusters
uv run kubestellar execute helm_deploy \
  -P operation=uninstall \
  -P release_name=old-app \
  -P target_clusters='["cluster1"]' \
  -P namespace=deprecated-apps
```

**Chart Update and Variable Management:**

```bash
# Update chart repository information
uv run kubestellar execute helm_deploy \
  -P operation=install \
  -P chart_name=postgresql \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P chart_version=latest \
  -P release_name=database \
  -P set_values='["auth.postgresPassword=newpassword","persistence.size=20Gi"]'

# Update with multiple variable sources
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=wordpress \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P values_files='["values-base.yaml","values-override.yaml"]' \
  -P set_values='["wordpressUsername=admin","wordpressEmail=admin@example.com"]' \
  -P cluster_set_values='["prod=wordpressBlogName=Prod Blog","staging=wordpressBlogName=Staging Blog"]' \
  -P target_clusters='["prod","staging"]'

# Update with environment-specific variables
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=app \
  -P chart_path=./charts/app \
  -P release_name=myapp \
  -P set_values='["global.environment=production","global.version=v2.1.0"]' \
  -P cluster_set_values='["us-east=global.region=us-east-1","eu-west=global.region=eu-west-1"]' \
  -P cluster_values='["us-east=values-us.yaml","eu-west=values-eu.yaml"]' \
  -P kubestellar_labels='{"version":"v2.1.0","environment":"production"}'

# Update with secret management
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=mysql \
  -P repository_url=https://charts.bitnami.com/bitnami \
  -P values_file=values-secrets.yaml \
  -P set_values='["auth.existingSecret=mysql-credentials"]' \
  -P target_clusters='["secure-cluster"]' \
  -P create_namespace=true \
  -P namespace=databases
```

**Advanced Examples:**

```bash
# Dry run deployment with full configuration
uv run kubestellar execute helm_deploy \
  -P chart_name=complex-app \
  -P chart_version=1.5.0 \
  -P repository_url=https://charts.example.com \
  -P target_clusters='["prod-us","prod-eu"]' \
  -P cluster_values='["prod-us=values-us.yaml","prod-eu=values-eu.yaml"]' \
  -P set_values='["global.environment=production"]' \
  -P cluster_set_values='["prod-us=region=us-east-1","prod-eu=region=eu-west-1"]' \
  -P create_binding_policy=true \
  -P cluster_selector_labels='{"environment":"production","region":"multi"}' \
  -P wait=true \
  -P timeout=10m \
  -P atomic=true \
  -P dry_run=true

# Install with multiple namespaces and binding policy
uv run kubestellar execute helm_deploy \
  -P chart_name=microservice \
  -P chart_path=/path/to/microservice-chart \
  -P target_namespaces='["frontend","backend","api"]' \
  -P create_namespace=true \
  -P binding_policy_name=microservice-binding \
  -P kubestellar_labels='{"app-type":"microservice","team":"platform"}'
```

**Variable Management and Update Patterns:**

The `helm_deploy` function supports sophisticated variable management for different scenarios:

**1. Variable Precedence (highest to lowest):**
```bash
# Order of precedence:
# 1. cluster_set_values (per-cluster --set values)
# 2. set_values (global --set values)  
# 3. cluster_values (per-cluster values files)
# 4. values_files (additional values files)
# 5. values_file (base values file)
# 6. Chart default values

# Example showing precedence
uv run kubestellar execute helm_deploy \
  -P chart_name=myapp \
  -P values_file=base-values.yaml \
  -P values_files='["environment-prod.yaml","security-hardened.yaml"]' \
  -P set_values='["global.environment=production"]' \
  -P cluster_values='["us-east=us-values.yaml","eu-west=eu-values.yaml"]' \
  -P cluster_set_values='["us-east=region.name=us-east-1","eu-west=region.name=eu-west-1"]'
```

**2. Update Strategies:**
```bash
# Rolling update with zero downtime
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=webapp \
  -P chart_version=2.1.0 \
  -P release_name=webapp-prod \
  -P set_values='["image.tag=v2.1.0","replicaCount=6"]' \
  -P wait=true \
  -P timeout=15m \
  -P atomic=false

# Blue-green deployment pattern
uv run kubestellar execute helm_deploy \
  -P operation=install \
  -P chart_name=webapp \
  -P chart_version=2.1.0 \
  -P release_name=webapp-blue \
  -P set_values='["service.selector.version=blue","image.tag=v2.1.0"]' \
  -P namespace=production

# Canary deployment
uv run kubestellar execute helm_deploy \
  -P operation=install \
  -P chart_name=webapp \
  -P release_name=webapp-canary \
  -P set_values='["replicaCount=1","service.weight=10","image.tag=v2.1.0"]' \
  -P kubestellar_labels='{"deployment-type":"canary","version":"v2.1.0"}'
```

**3. Configuration Management:**
```bash
# Environment-specific updates
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=api-service \
  -P cluster_set_values='[
    "prod=database.host=prod-db.example.com",
    "prod=database.replicas=3",
    "staging=database.host=staging-db.example.com", 
    "staging=database.replicas=1",
    "dev=database.host=dev-db.example.com",
    "dev=database.replicas=1"
  ]' \
  -P target_clusters='["prod","staging","dev"]'

# Resource scaling updates
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P release_name=monitoring-stack \
  -P cluster_set_values='[
    "large-cluster=prometheus.resources.requests.memory=4Gi",
    "large-cluster=prometheus.storage.size=100Gi",
    "small-cluster=prometheus.resources.requests.memory=2Gi",
    "small-cluster=prometheus.storage.size=50Gi"
  ]' \
  -P set_values='["prometheus.retention=30d"]'

# Feature flag updates
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=feature-service \
  -P set_values='[
    "features.newUI=true",
    "features.advancedSearch=false", 
    "features.experimentalAPI=true"
  ]' \
  -P kubestellar_labels='{"feature-flags":"updated","deployment-id":"$(date +%s)"}'
```

**4. Multi-Environment Updates:**
```bash
# Staged rollout across environments
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=backend-service \
  -P chart_version=1.5.2 \
  -P cluster_values='[
    "dev=values-dev.yaml",
    "staging=values-staging.yaml", 
    "prod=values-prod.yaml"
  ]' \
  -P cluster_set_values='[
    "dev=replicas=1",
    "staging=replicas=2",
    "prod=replicas=5"
  ]' \
  -P target_clusters='["dev","staging","prod"]' \
  -P wait=true

# Region-specific updates with different configurations
uv run kubestellar execute helm_deploy \
  -P operation=upgrade \
  -P chart_name=cdn-service \
  -P cluster_set_values='[
    "us-east=region=us-east-1,cdn.endpoint=https://us-cdn.example.com",
    "us-west=region=us-west-2,cdn.endpoint=https://west-cdn.example.com",
    "eu-central=region=eu-central-1,cdn.endpoint=https://eu-cdn.example.com"
  ]' \
  -P cluster_selector_labels='{"region":"multi","service":"cdn"}'
```

**Agent Mode Examples:**
```bash
# Start agent mode
uv run kubestellar agent

# Natural language Helm queries
[openai] ▶ deploy nginx ingress using helm to all production clusters
[openai] ▶ install prometheus helm chart with custom values for monitoring
[openai] ▶ upgrade myapp helm release to version 2.0 with new database settings
[openai] ▶ update the webapp chart with increased replicas for high traffic
[openai] ▶ show me the status of all helm releases
[openai] ▶ rollback the api-service helm release to previous version
[openai] ▶ create a binding policy for helm deployed applications
[openai] ▶ update chart variables for different environments
```

### Core Functions

#### get_kubeconfig

Retrieves and analyzes kubeconfig file information.

**Parameters:**
- `kubeconfig_path` (string, optional): Path to kubeconfig file
- `context` (string, optional): Specific context to analyze
- `detail_level` (string, optional): Level of detail (`summary`, `full`, `contexts`)

**Examples:**
```bash
# Get summary of current kubeconfig  
uv run kubestellar execute get_kubeconfig

# Get full cluster details
uv run kubestellar execute get_kubeconfig -P detail_level=full

# Check specific context
uv run kubestellar execute get_kubeconfig -P context=production
```

### Multi-Cluster Management Functions

#### multicluster_create

Create Kubernetes resources across multiple clusters with namespace targeting.

**Key Parameters:**
- `resource_type` & `resource_name`: Resource to create
- `all_namespaces`: Deploy across all namespaces
- `target_namespaces`: Specific namespace list
- `namespace_selector`: Label-based namespace targeting

**Examples:**
```bash
# Create deployment across all namespaces
uv run kubestellar execute multicluster_create \
  -P resource_type=deployment \
  -P resource_name=web-app \
  -P image=nginx:1.21 \
  -P all_namespaces=true \
  -P dry_run=client

# Create in specific namespaces
uv run kubestellar execute multicluster_create \
  -P resource_type=configmap \
  -P resource_name=app-config \
  -P target_namespaces='["prod","staging"]'
```

#### multicluster_logs

Aggregate logs from containers across multiple clusters and namespaces.

**Key Parameters:**
- `all_namespaces`: Get logs from all namespaces
- `target_namespaces`: Specific namespace list
- `label_selector`: Pod label filtering
- `follow`: Stream logs continuously

**Examples:**
```bash
# Get logs from all namespaces
uv run kubestellar execute multicluster_logs \
  -P all_namespaces=true \
  -P label_selector="app=nginx" \
  -P tail=100

# Get logs from specific namespaces
uv run kubestellar execute multicluster_logs \
  -P target_namespaces='["production"]' \
  -P pod_name=web-server
```

#### deploy_to

Deploy resources to specific clusters with advanced namespace targeting.

**Key Parameters:**
- `target_clusters`: Specific clusters to deploy to
- `all_namespaces`: Deploy across all namespaces
- `target_namespaces`: Specific namespace list
- `dry_run`: Test deployment without execution

**Examples:**
```bash
# Deploy to specific clusters and namespaces
uv run kubestellar execute deploy_to \
  -P target_clusters='["cluster1","cluster2"]' \
  -P resource_type=deployment \
  -P resource_name=api-server \
  -P image=myapp:v1.0 \
  -P target_namespaces='["frontend","backend"]' \
  -P dry_run=true

# List available clusters
uv run kubestellar execute deploy_to -P list_clusters=true
```

### Resource Discovery Functions

#### gvrc_discovery

Discover available Kubernetes resources, their versions, and categories across clusters.

**Key Parameters:**
- `resource_filter`: Filter by resource name pattern
- `all_namespaces`: Include namespace discovery
- `api_resources`: Include built-in API resources
- `custom_resources`: Include custom resources (CRDs)
- `output_format`: Response format (`summary`, `detailed`, `json`)

**Examples:**
```bash
# Discover all resources across clusters
uv run kubestellar execute gvrc_discovery

# Filter by resource pattern
uv run kubestellar execute gvrc_discovery \
  -P resource_filter=pod \
  -P output_format=detailed

# Discover only custom resources
uv run kubestellar execute gvrc_discovery \
  -P api_resources=false \
  -P custom_resources=true
```

#### namespace_utils

Manage namespaces and namespace-scoped resources across multiple clusters.

**Key Parameters:**
- `operation`: Operation to perform (`list`, `get`, `list-resources`)
- `all_namespaces`: Include all namespaces
- `namespace_selector`: Label-based namespace filtering
- `include_resources`: Include resources within namespaces

**Examples:**
```bash
# List all namespaces across clusters
uv run kubestellar execute namespace_utils \
  -P operation=list \
  -P all_namespaces=true

# Get details for specific namespaces
uv run kubestellar execute namespace_utils \
  -P operation=get \
  -P namespace_names='["production","staging"]'

# List resources in all namespaces
uv run kubestellar execute namespace_utils \
  -P operation=list-resources \
  -P all_namespaces=true \
  -P resource_types='["pods","services"]'
```

## Development

### Project Structure

```
a2a/
├── src/
│   ├── shared/                         # Shared components
│   │   ├── __init__.py
│   │   ├── base_functions.py           # Base classes and registry
│   │   └── functions/                  # Function implementations
│   │       ├── __init__.py             # Function registration
│   │       ├── kubeconfig.py           # Kubeconfig analysis
│   │       ├── kubestellar_management.py # KubeStellar management with 2024 architecture
│   │       ├── helm_deploy.py          # Helm chart deployment with binding policies (NEW)
│   │       ├── multicluster_create.py  # Multi-cluster resource creation
│   │       ├── multicluster_logs.py    # Multi-cluster log aggregation
│   │       ├── deploy_to.py            # Selective cluster deployment
│   │       ├── gvrc_discovery.py       # GVRC resource discovery
│   │       └── namespace_utils.py      # Namespace management
│   ├── mcp/                            # MCP server implementation
│   │   ├── __init__.py
│   │   └── server.py                   # MCP server entry point
│   └── a2a/                            # CLI implementation
│       ├── __init__.py
│       └── cli.py                      # CLI entry point
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── test_base_functions.py          # Base function tests
│   ├── test_cli.py                     # CLI tests
│   ├── test_kubeconfig.py              # Kubeconfig tests
│   ├── test_helm_deploy.py             # Helm deployment tests (NEW)
│   ├── test_kubestellar_management.py  # KubeStellar management tests  
│   ├── test_gvrc_discovery.py          # GVRC discovery tests
│   └── test_namespace_utils.py         # Namespace utils tests
├── docs/                               # Documentation
│   ├── adding_functions.md             # Function development guide
│   ├── ci_implementation.md            # CI/CD documentation
│   └── multi_namespace_gvrc_support.md # Multi-namespace & GVRC guide
├── pyproject.toml                      # Project configuration
├── README.md                           # This file
├── LICENSE                             # License file
├── OWNERS                              # Project ownership
└── uv.lock                             # Dependency lock file
```

### Adding New Functions

See [docs/adding_functions.md](docs/adding_functions.md) for a comprehensive guide. Quick overview:

1. Create a new file in `src/shared/functions/`
2. Implement a class inheriting from `BaseFunction`
3. Register it in `src/shared/functions/__init__.py`

Example:

```python
# src/shared/functions/my_function.py
from typing import Any, Dict
from ..base_functions import BaseFunction

class MyFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="my_function",
            description="Description of what this function does"
        )
    
    async def execute(self, param1: str) -> Dict[str, Any]:
        # Implementation
        return {"result": f"Processed {param1}"}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        }
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_kubeconfig.py

# Run with verbose output
uv run pytest -v
```

**Test Status**: ✅ All 60+ tests passing
- CLI tests: 9 tests passing
- Base function tests: 8 tests passing  
- Kubeconfig function tests: 8 tests passing
- **Helm deployment tests: 35 tests passing** ✨ **NEW**
- KubeStellar management tests: Various integration tests
- GVRC discovery tests: Resource discovery validation
- Namespace utilities tests: Multi-namespace functionality

### Code Quality & Linting

This project uses several tools to maintain code quality and consistency. All checks are automatically run in CI, but you can run them locally during development.

#### Individual Tools

```bash
# Format code with Black
uv run black src/ tests/

# Check formatting (without changing files)
uv run black --check src/ tests/

# Lint code with Ruff (fast Python linter)
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check src/ tests/ --fix

# Sort imports with isort
uv run isort src/ tests/

# Check import sorting (without changing files)  
uv run isort --check-only src/ tests/

# Type check with mypy
uv run mypy src/

# Security scan with bandit
uv run bandit -r src/

# Check for dependency vulnerabilities
uv run safety check
```

#### Combined Quality Checks

```bash
# Run all formatting and linting checks
uv run black --check src/ tests/ && \
uv run isort --check-only src/ tests/ && \
uv run ruff check src/ tests/ && \
uv run mypy src/

# Fix all auto-fixable issues
uv run black src/ tests/ && \
uv run isort src/ tests/ && \
uv run ruff check src/ tests/ --fix

# Run complete quality check (like CI)
uv run pytest tests/ -v && \
uv run black --check src/ tests/ && \
uv run isort --check-only src/ tests/ && \
uv run ruff check src/ tests/ && \
uv run mypy src/ --ignore-missing-imports && \
uv run bandit -r src/ -ll
```

#### Pre-commit Workflow

Before committing code, run:

```bash
# 1. Format and fix issues
uv run black src/ tests/
uv run isort src/ tests/  
uv run ruff check src/ tests/ --fix

# 2. Run tests
uv run pytest tests/ -v

# 3. Verify all checks pass
uv run black --check src/ tests/
uv run isort --check-only src/ tests/
uv run ruff check src/ tests/
```

#### Tool Configuration

All tools are configured in `pyproject.toml`:

- **Black**: Line length 88, Python 3.11+ target
- **Ruff**: Fast linting with comprehensive rule set
- **isort**: Black-compatible import sorting
- **mypy**: Strict type checking enabled
- **bandit**: Security linting for Python code
- **coverage**: Test coverage reporting

### Development Workflow

1. Create a new branch for your feature
2. Add your function following the guide
3. Write tests for your function
4. Ensure all quality checks pass
5. Submit a pull request

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create your branch from `main`
2. **Write tests** for any new functionality
3. **Update documentation** as needed
4. **Follow the code style** (use black and ruff)
5. **Write clear commit messages**
6. **Submit a pull request** with a clear description

### Commit Message Format

```
type: subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: add pod listing function

Adds a new function to list pods across all namespaces with filtering
options for status and labels.

Closes #123
```

## Troubleshooting

### Common Issues

#### Function not found

```bash
Error: Function 'my_function' not found.
```

**Solution**: Ensure the function is registered in `src/shared/functions/__init__.py`

#### Import errors

```bash
ModuleNotFoundError: No module named 'kubestellar'
```

**Solution**: Install the package in development mode: `uv pip install -e .`

#### MCP server not connecting

**Solution**: 
1. Check Claude Desktop logs
2. Verify the path in configuration is absolute
3. Ensure Python and uv are in PATH

#### Kubeconfig not found

```bash
{"error": "Kubeconfig file not found at: /home/user/.kube/config"}
```

**Solution**: 
1. Ensure kubectl is configured
2. Set KUBECONFIG environment variable
3. Pass explicit path: `--param kubeconfig_path=/path/to/config`

### Debug Mode

Enable debug logging:

```bash
# For CLI
LOG_LEVEL=DEBUG uv run kubestellar execute get_kubeconfig

# For MCP server (in config)
"env": {
  "LOG_LEVEL": "DEBUG"
}
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/kubestellar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kubestellar/discussions)
- **Documentation**: [Full documentation](https://kubestellar.io/docs)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [MCP SDK](https://github.com/anthropics/mcp-sdk)
- Inspired by the KubeStellar project for multi-cluster Kubernetes management
- Thanks to all contributors and the open-source community

---

Made with ❤️ by the KubeStellar community