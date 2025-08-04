"""Function implementations."""

from ..base_functions import function_registry
from .kubeconfig import KubeconfigFunction


def initialize_functions():
    """Initialize and register all available functions."""
    # Register kubeconfig function
    function_registry.register(KubeconfigFunction())

    # Add more function registrations here as they are created
