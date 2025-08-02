"""A2A Agent CLI implementation."""

import asyncio
import json
import click
from typing import Any, Dict, Optional

from ..shared.base_functions import function_registry, async_to_sync
from ..shared.functions import initialize_functions


@click.group()
@click.pass_context
def cli(ctx):
    """KubeStellar Agent - Execute functions from command line."""
    # Initialize functions when CLI starts
    initialize_functions()
    ctx.ensure_object(dict)


@cli.command()
def list_functions():
    """List all available functions."""
    functions = function_registry.list_all()
    if not functions:
        click.echo("No functions registered.")
        return
    
    click.echo("Available functions:")
    for func in functions:
        click.echo(f"\n- {func.name}")
        click.echo(f"  Description: {func.description}")
        schema = func.get_schema()
        if schema.get("properties"):
            click.echo("  Parameters:")
            for param, details in schema["properties"].items():
                required = param in schema.get("required", [])
                req_str = " (required)" if required else " (optional)"
                click.echo(f"    - {param}: {details.get('type', 'any')}{req_str}")
                if "description" in details:
                    click.echo(f"      {details['description']}")


@cli.command()
@click.argument('function_name')
@click.option('--params', '-p', help='JSON string of parameters')
@click.option('--param', '-P', multiple=True, help='Key=value parameter pairs')
def execute(function_name: str, params: Optional[str], param: tuple):
    """Execute a specific function."""
    function = function_registry.get(function_name)
    if not function:
        click.echo(f"Error: Function '{function_name}' not found.", err=True)
        click.echo("Use 'list-functions' to see available functions.", err=True)
        return
    
    # Parse parameters
    kwargs: Dict[str, Any] = {}
    
    if params:
        try:
            kwargs = json.loads(params)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON parameters: {e}", err=True)
            return
    
    # Parse key=value pairs
    for p in param:
        if '=' not in p:
            click.echo(f"Error: Invalid parameter format '{p}'. Use key=value", err=True)
            return
        key, value = p.split('=', 1)
        # Try to parse as JSON, fallback to string
        try:
            kwargs[key] = json.loads(value)
        except json.JSONDecodeError:
            kwargs[key] = value
    
    # Execute function
    try:
        # Convert async function to sync for CLI
        if asyncio.iscoroutinefunction(function.execute):
            result = async_to_sync(function.execute)(**kwargs)
        else:
            result = function.execute(**kwargs)
        
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error executing function: {e}", err=True)


@cli.command()
@click.argument('function_name')
def describe(function_name: str):
    """Get detailed information about a function."""
    function = function_registry.get(function_name)
    if not function:
        click.echo(f"Error: Function '{function_name}' not found.", err=True)
        return
    
    click.echo(f"Function: {function.name}")
    click.echo(f"Description: {function.description}")
    click.echo("\nSchema:")
    click.echo(json.dumps(function.get_schema(), indent=2))


def main():
    """Main entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()