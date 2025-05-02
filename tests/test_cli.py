"""
Tests for the CLI module
"""
import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

# Import the module to test
from aznuke.cli import parse_resource_types, cmd_scan, cmd_delete


def test_parse_resource_types():
    """Test parsing resource types from a comma-separated string"""
    # Parse resource types from a string
    result = parse_resource_types("storage,virtualmachines,keyvault")
    
    # Verify the result
    assert result == ["storage", "virtualmachines", "keyvault"]


def test_parse_resource_types_none():
    """Test parsing resource types when the input is None"""
    # Parse resource types from None
    result = parse_resource_types(None)
    
    # Verify the result
    assert result is None


@pytest.mark.asyncio
@patch('aznuke.cli.show_startup_animation')
@patch('azure.identity.DefaultAzureCredential')
@patch('aznuke.cli.async_spinner')
@patch('aznuke.cli.parse_resource_types')
@patch('aznuke.cli.load_exclusions')
@patch('aznuke.cli.create_progress_bar')
@patch('aznuke.cli.filter_resources_async')
@patch('aznuke.cli.show_summary_by_type')
async def test_cmd_scan(
    mock_show_summary,
    mock_filter_async,
    mock_progress_bar,
    mock_load_exclusions,
    mock_parse_types,
    mock_spinner,
    mock_credentials,
    mock_startup,
):
    """Test the scan command"""
    # Configure mocks
    mock_creds_instance = MagicMock()
    mock_credentials.return_value = mock_creds_instance
    
    mock_subscription = MagicMock()
    mock_subscription.display_name = "development"
    mock_subscriptions = [mock_subscription]
    
    mock_spinner_instance = AsyncMock()
    mock_spinner_instance.return_value = mock_subscriptions
    mock_spinner.return_value = mock_subscriptions
    
    mock_resource = MagicMock()
    mock_resources = [mock_resource]
    
    # Configure the second spinner call to return resources
    mock_spinner.side_effect = [mock_subscriptions, mock_resources]
    
    mock_exclusions = {"resource_types": ["Microsoft.KeyVault/vaults"]}
    mock_load_exclusions.return_value = mock_exclusions
    
    mock_progress_instance = MagicMock()
    mock_progress_bar.return_value = mock_progress_instance
    
    mock_resources_to_process = [mock_resource]
    mock_resources_to_preserve = []
    mock_filter_async.return_value = (mock_resources_to_process, mock_resources_to_preserve)
    
    # Configure the arguments
    args = MagicMock()
    args.profile = "development"
    args.region = None
    args.checks = None
    args.output = "text"
    args.severity = None
    args.config = "config/exclusions.yaml"
    args.verbose = False
    
    # Call the function
    await cmd_scan(args)
    
    # Verify the function calls
    mock_startup.assert_called_once()
    mock_credentials.assert_called_once()
    assert mock_spinner.call_count == 2
    mock_load_exclusions.assert_called_once_with(args.config)
    mock_progress_bar.assert_called_once()
    mock_filter_async.assert_called_once()
    mock_show_summary.assert_called_once()


@pytest.mark.asyncio
@patch('aznuke.cli.show_startup_animation')
@patch('azure.identity.DefaultAzureCredential')
@patch('aznuke.cli.async_spinner')
@patch('aznuke.cli.parse_resource_types')
@patch('aznuke.cli.load_exclusions')
@patch('aznuke.cli.create_progress_bar')
@patch('aznuke.cli.filter_resources_async')
@patch('aznuke.cli.show_summary_by_type')
@patch('aznuke.cli.require_confirmation')
@patch('aznuke.cli.delete_resources')
@patch('aznuke.cli.show_completion_animation')
async def test_cmd_delete(
    mock_completion,
    mock_delete,
    mock_confirmation,
    mock_show_summary,
    mock_filter_async,
    mock_progress_bar,
    mock_load_exclusions,
    mock_parse_types,
    mock_spinner,
    mock_credentials,
    mock_startup,
):
    """Test the delete command"""
    # Configure mocks
    mock_creds_instance = MagicMock()
    mock_credentials.return_value = mock_creds_instance
    
    mock_subscription = MagicMock()
    mock_subscription.display_name = "development"
    mock_subscriptions = [mock_subscription]
    
    mock_spinner.side_effect = [mock_subscriptions, [MagicMock()]]
    
    mock_exclusions = {"resource_types": ["Microsoft.KeyVault/vaults"]}
    mock_load_exclusions.return_value = mock_exclusions
    
    mock_progress_instance = MagicMock()
    mock_progress_bar.return_value = mock_progress_instance
    
    mock_resources_to_delete = [MagicMock()]
    mock_resources_to_preserve = []
    mock_filter_async.return_value = (mock_resources_to_delete, mock_resources_to_preserve)
    
    mock_confirmation.return_value = True
    
    mock_deleted = [MagicMock()]
    mock_failed = []
    mock_delete.return_value = (mock_deleted, mock_failed)
    
    # Configure the arguments
    args = MagicMock()
    args.profile = "development"
    args.region = None
    args.checks = None
    args.dry_run = False
    args.config = "config/exclusions.yaml"
    args.protected_subscriptions = None
    args.yes = False
    args.verbose = False
    
    # Call the function
    await cmd_delete(args)
    
    # Verify the function calls
    mock_startup.assert_called_once()
    mock_credentials.assert_called_once()
    assert mock_spinner.call_count == 2
    mock_load_exclusions.assert_called_once_with(args.config)
    mock_progress_bar.assert_called_once()
    mock_filter_async.assert_called_once()
    mock_show_summary.assert_called_once()
    mock_confirmation.assert_called_once()
    mock_delete.assert_called_once()
    mock_completion.assert_called_once_with(True, len(mock_deleted), len(mock_failed)) 