# KubeStellar

A powerful, unified implementation of both MCP (Model Context Protocol) server and KubeStellar Agent CLI tool with shared functions for Kubernetes multi-cluster management and orchestration.

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

## Overviewcxxc

KubeStellar is a comprehensive tool designed to simplify Kubernetes multi-cluster management through a dual-interface approach:

1. **CLI Interface**: Direct command-line access for developers and operators
2. **MCP Server**: Integration with AI assistants like Claude Desktop for intelligent cluster management

The tool provides a shared function architecture, ensuring consistency between both interfaces while enabling powerful automation and management capabilities.

## Features

- 🔄 **Dual Interface**: Use the same functions via CLI or through AI assistants
- 🌐 **Multi-Cluster Support**: Manage multiple Kubernetes clusters from a single interface
- 🔧 **Extensible Architecture**: Easy to add new functions and capabilities
- 🔒 **Type-Safe**: Full type hints and schema validation for reliability
- 🚀 **Async Support**: Built with modern async/await patterns for performance
- 📝 **Rich Documentation**: Comprehensive guides for users and developers
- 🧪 **Well-Tested**: Includes comprehensive test suite with 100% passing tests
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
```

### MCP Server Quick Start

1. Add to Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kubestellar": {
      "command": "uv",
      "args": ["run", "kubestellar-mcp"],
      "cwd": "/path/to/kubestellar"
    }
  }
}
```

2. Restart Claude Desktop
3. Start using KubeStellar functions in your conversations

## Usage

### KubeStellar CLI

The CLI provides several commands for interacting with functions:

#### List Functions

```bash
kubestellar list-functions
```

Output:
```
Available functions:

- get_kubeconfig
  Description: Get details from kubeconfig file including contexts, clusters, and users
  Parameters:
    - kubeconfig_path: string (optional)
      Path to kubeconfig file (defaults to ~/.kube/config or $KUBECONFIG)
    - context: string (optional)
      Specific context to get details for
    - detail_level: string (optional)
      Level of detail to return
```

#### Execute Functions

```bash
# Basic execution
uv run kubestellar execute <function_name>

# With parameters using --param
uv run kubestellar execute get_kubeconfig --param context=production --param detail_level=full

# With JSON parameters
uv run kubestellar execute get_kubeconfig --params '{"context": "production", "detail_level": "full"}'

# Mixed parameters
uv run kubestellar execute get_kubeconfig --param context=staging --params '{"detail_level": "contexts"}'
```

#### Describe Functions

```bash
uv run kubestellar describe get_kubeconfig
```

Output:
```
Function: get_kubeconfig
Description: Get details from kubeconfig file including contexts, clusters, and users

Schema:
{
  "type": "object",
  "properties": {
    "kubeconfig_path": {
      "type": "string",
      "description": "Path to kubeconfig file (defaults to ~/.kube/config or $KUBECONFIG)"
    },
    "context": {
      "type": "string",
      "description": "Specific context to get details for"
    },
    "detail_level": {
      "type": "string",
      "enum": ["summary", "full", "contexts"],
      "description": "Level of detail to return",
      "default": "summary"
    }
  },
  "required": []
}
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

### get_kubeconfig

Retrieves and analyzes kubeconfig file information.

**Parameters:**
- `kubeconfig_path` (string, optional): Path to kubeconfig file
  - Default: `~/.kube/config` or `$KUBECONFIG` environment variable
- `context` (string, optional): Specific context to analyze
- `detail_level` (string, optional): Level of detail in response
  - Options: `"summary"`, `"full"`, `"contexts"`
  - Default: `"summary"`

**Examples:**

```bash
# Get summary of current kubeconfig
uv run kubestellar execute get_kubeconfig

# Get full details
uv run kubestellar execute get_kubeconfig --param detail_level=full

# Check specific context
uv run kubestellar execute get_kubeconfig --param context=production

# Use custom kubeconfig file
uv run kubestellar execute get_kubeconfig --param kubeconfig_path=/path/to/config
```

**Response Format:**
```json
{
  "kubeconfig_path": "/home/user/.kube/config",
  "current_context": "production",
  "contexts": ["development", "staging", "production"],
  "total_contexts": 3,
  "clusters": [...],
  "users": [...]
}
```

## Development

### Project Structure

```
kubestellar/
├── src/
│   ├── shared/                    # Shared components
│   │   ├── __init__.py
│   │   ├── base_functions.py      # Base classes and registry
│   │   └── functions/             # Function implementations
│   │       ├── __init__.py        # Function initialization
│   │       └── kubeconfig.py      # Kubeconfig function
│   ├── mcp/                       # MCP server implementation
│   │   ├── __init__.py
│   │   └── server.py              # MCP server entry point
│   └── a2a/                       # CLI implementation
│       ├── __init__.py
│       └── cli.py                 # CLI entry point
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_kubeconfig.py
│   └── test_base_functions.py
├── docs/                          # Documentation
│   └── adding_functions.md        # Function development guide
├── examples/                      # Example usage
│   └── example_function.py
├── pyproject.toml                 # Project configuration
├── README.md                      # This file
├── LICENSE                        # License file
└── .gitignore                     # Git ignore rules
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

**Test Status**: ✅ All 25 tests passing
- CLI tests: 9 tests passing
- Base function tests: 8 tests passing  
- Kubeconfig function tests: 8 tests passing

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff src/ tests/

# Type check
uv run mypy src/

# Run all checks
uv run black src/ tests/ && uv run ruff src/ tests/ && uv run mypy src/
```

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
