# auth.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient

def get_credentials():
    """Authenticate using DefaultAzureCredential."""
    return DefaultAzureCredential()

def get_subscriptions(credentials):
    """Get all Azure subscriptions the authenticated user has access to."""
    subscription_client = SubscriptionClient(credentials)
    return list(subscription_client.subscriptions.list())

def get_resource_client(credentials, subscription_id):
    """Create a resource management client for a specific subscription."""
    return ResourceManagementClient(credentials, subscription_id)