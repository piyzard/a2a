"""Function implementations."""

from ..base_functions import function_registry
from .kubeconfig import KubeconfigFunction
from .multicluster_create import MultiClusterCreateFunction
from .multicluster_logs import MultiClusterLogsFunction
from .deploy_to import DeployToFunction


def initialize_functions():
    """Initialize and register all available functions."""
    # Register kubeconfig function
    function_registry.register(KubeconfigFunction())
    
    # Register KubeStellar multi-cluster functions
    function_registry.register(MultiClusterCreateFunction())
    function_registry.register(MultiClusterLogsFunction())
    function_registry.register(DeployToFunction())
    
    # Add more function registrations here as they are created
