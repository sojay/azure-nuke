# discovery.py
from aznuke.src.auth import get_resource_client

def discover_resources(resource_client, resource_types=None):
    """
    Discover resources in a subscription.
    
    Args:
        resource_client: The Azure resource client
        resource_types: Optional list of resource types to filter by
    """
    if resource_types:
        # Filter resources by type if specific types are requested
        resources = []
        for resource_type in resource_types:
            # Azure resource types are case-sensitive
            filter_str = f"resourceType eq '{resource_type}'"
            filtered_resources = list(resource_client.resources.list(filter=filter_str))
            resources.extend(filtered_resources)
        return resources
    else:
        # Get all resources if no specific types are requested
        resources = list(resource_client.resources.list())
        return resources

def discover_all_resources(credentials, subscriptions, resource_types=None):
    """
    Discover all resources across all subscriptions.
    
    Args:
        credentials: Azure credentials
        subscriptions: List of subscriptions to scan
        resource_types: Optional list of resource types to filter by
    """
    all_resources = []
    
    for subscription in subscriptions:
        resource_client = get_resource_client(credentials, subscription.subscription_id)
        resources = discover_resources(resource_client, resource_types)
        
        # Enhance resources with subscription info
        for resource in resources:
            resource.subscription_id = subscription.subscription_id
            resource.subscription_name = subscription.display_name
            all_resources.append(resource)
    
    return all_resources