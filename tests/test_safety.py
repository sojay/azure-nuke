"""
Tests for the safety module
"""
import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

from aznuke.src.safety import is_protected_subscription, require_confirmation

def test_is_protected_subscription():
    """Test identifying protected subscriptions"""
    # Test with a protected subscription ID
    subscription_id = "00000000-0000-0000-0000-000000000000"
    protected_ids = ["11111111-1111-1111-1111-111111111111", "00000000-0000-0000-0000-000000000000"]
    
    # Verify the function identifies the protected subscription
    assert is_protected_subscription(subscription_id, protected_ids) is True
    
    # Test with a non-protected subscription ID
    subscription_id = "22222222-2222-2222-2222-222222222222"
    
    # Verify the function doesn't identify a non-protected subscription
    assert is_protected_subscription(subscription_id, protected_ids) is False

@pytest.mark.asyncio
@patch('builtins.input')
@patch('builtins.print')
@patch('aznuke.src.safety.delete_resources')
async def test_require_confirmation_yes(mock_delete_resources, mock_print, mock_input):
    """Test confirmation of deletion when the user confirms"""
    # Configure the mock resources
    mock_resource = MagicMock()
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    mock_resource.name = "teststorage"
    mock_resource.subscription_name = "Development"
    
    resources_to_delete = [mock_resource]
    
    # Configure user input to confirm deletion
    mock_input.return_value = "DELETE"
    
    # Configure the delete_resources function
    mock_delete_resources.return_value = (resources_to_delete, [])
    
    # Create mock credentials
    mock_credentials = MagicMock()
    
    # Call the function
    result = await require_confirmation(resources_to_delete, mock_credentials)
    
    # Verify the function behavior
    assert mock_input.call_count == 1
    assert mock_delete_resources.call_count == 1
    assert mock_print.call_count > 0

@pytest.mark.asyncio
@patch('builtins.input')
@patch('builtins.print')
@patch('aznuke.src.safety.delete_resources')
async def test_require_confirmation_no(mock_delete_resources, mock_print, mock_input):
    """Test cancellation of deletion when the user doesn't confirm"""
    # Configure the mock resources
    mock_resource = MagicMock()
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    mock_resource.name = "teststorage"
    mock_resource.subscription_name = "Development"
    
    resources_to_delete = [mock_resource]
    
    # Configure user input to deny deletion
    mock_input.return_value = "NO"
    
    # Create mock credentials
    mock_credentials = MagicMock()
    
    # Call the function
    result = await require_confirmation(resources_to_delete, mock_credentials)
    
    # Verify the function behavior
    assert result is False
    assert mock_input.call_count == 1
    assert mock_delete_resources.call_count == 0
    assert mock_print.call_count > 0

@pytest.mark.asyncio
@patch('builtins.print')
async def test_require_confirmation_dry_run(mock_print):
    """Test confirmation in dry run mode"""
    # Configure the mock resources
    mock_resource = MagicMock()
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    mock_resource.name = "teststorage"
    mock_resource.subscription_name = "Development"
    
    resources_to_delete = [mock_resource]
    
    # Create mock credentials
    mock_credentials = MagicMock()
    
    # Call the function in dry run mode
    result = await require_confirmation(resources_to_delete, mock_credentials, dry_run=True)
    
    # Verify the function behavior
    assert result is True
    assert mock_print.call_count > 0

@pytest.mark.asyncio
@patch('builtins.print')
async def test_require_confirmation_empty(mock_print):
    """Test confirmation with empty resources list"""
    # Create an empty list of resources
    resources_to_delete = []
    
    # Create mock credentials
    mock_credentials = MagicMock()
    
    # Call the function
    result = await require_confirmation(resources_to_delete, mock_credentials)
    
    # Verify the function behavior
    assert result is False
    assert mock_print.call_count > 0 