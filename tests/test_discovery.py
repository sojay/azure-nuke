"""
Tests for the discovery module
"""
import pytest
from unittest.mock import MagicMock, patch

# Import the module to test
from aznuke.src.discovery import discover_resources, discover_all_resources


def test_discover_resources():
    """Test discovering resources in a subscription"""
    # Create a mock resource client
    mock_client = MagicMock()
    
    # Configure the mock client to return a list of resources
    mock_resources = [MagicMock(), MagicMock()]
    mock_client.resources.list.return_value = mock_resources
    
    # Call the function
    result = discover_resources(mock_client)
    
    # Verify the result
    assert result == mock_resources
    mock_client.resources.list.assert_called_once()


def test_discover_resources_with_resource_types():
    """Test discovering resources with resource type filtering"""
    # Create a mock resource client
    mock_client = MagicMock()
    
    # Configure the mock client to return different resources for different filters
    mock_resource1 = MagicMock()
    mock_resource2 = MagicMock()
    
    # Different resource types will return different resources
    def list_side_effect(filter=None):
        if filter == "resourceType eq 'Microsoft.Storage/storageAccounts'":
            return [mock_resource1]
        elif filter == "resourceType eq 'Microsoft.KeyVault/vaults'":
            return [mock_resource2]
        else:
            return []
    
    mock_client.resources.list.side_effect = list_side_effect
    
    # Call the function with resource types
    resource_types = ["Microsoft.Storage/storageAccounts", "Microsoft.KeyVault/vaults"]
    result = discover_resources(mock_client, resource_types)
    
    # Verify the result
    assert len(result) == 2
    assert mock_resource1 in result
    assert mock_resource2 in result
    assert mock_client.resources.list.call_count == 2


@patch('aznuke.src.discovery.get_resource_client')
def test_discover_all_resources(mock_get_client, mock_credentials, mock_subscription):
    """Test discovering all resources across subscriptions"""
    # Create a mock resource client
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    # Configure the mock client to return a list of resources
    mock_resource = MagicMock()
    mock_client.resources.list.return_value = [mock_resource]
    
    # Call the function
    subscriptions = [mock_subscription]
    result = discover_all_resources(mock_credentials, subscriptions)
    
    # Verify the result
    assert len(result) == 1
    assert result[0] == mock_resource
    assert result[0].subscription_id == mock_subscription.subscription_id
    assert result[0].subscription_name == mock_subscription.display_name
    mock_get_client.assert_called_once_with(mock_credentials, mock_subscription.subscription_id)


@patch('aznuke.src.discovery.get_resource_client')
def test_discover_all_resources_with_resource_types(mock_get_client, mock_credentials, mock_subscription):
    """Test discovering all resources with resource type filtering"""
    # Create a mock resource client
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    # Configure the mock client to return a list of resources
    mock_resource = MagicMock()
    mock_client.resources.list.return_value = [mock_resource]
    
    # Call the function with resource types
    subscriptions = [mock_subscription]
    resource_types = ["Microsoft.Storage/storageAccounts"]
    result = discover_all_resources(mock_credentials, subscriptions, resource_types)
    
    # Verify the result
    assert len(result) == 1
    assert result[0] == mock_resource
    assert result[0].subscription_id == mock_subscription.subscription_id
    assert result[0].subscription_name == mock_subscription.display_name
    mock_get_client.assert_called_once_with(mock_credentials, mock_subscription.subscription_id) 