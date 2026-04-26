"""
Tests for the CLI module
"""
import pytest
import inspect
from unittest.mock import MagicMock, patch

# Import the module to test
from aznuke.cli import create_parser, parse_resource_types, cmd_scan, cmd_delete


def spinner_results(*results):
    """Return an async_spinner side effect that closes unused coroutine args."""
    remaining = list(results)

    def side_effect(*args, **kwargs):
        coro = args[1] if len(args) > 1 else kwargs.get("coro")
        if inspect.iscoroutine(coro):
            coro.close()
        return remaining.pop(0)

    return side_effect


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


def test_create_parser_scan_uses_supplied_default_config():
    """Test scan parser wiring and configurable default config path."""
    parser = create_parser(default_config_path="/tmp/exclusions.yaml", version_string="Azure Nuke test")

    args = parser.parse_args(["scan", "--profile", "development", "--output", "json"])

    assert args.command == "scan"
    assert args.profile == "development"
    assert args.output == "json"
    assert args.config == "/tmp/exclusions.yaml"


def test_create_parser_delete_wires_safety_options():
    """Test delete parser wiring for dry-run and protected subscriptions."""
    parser = create_parser(default_config_path="/tmp/exclusions.yaml", version_string="Azure Nuke test")

    args = parser.parse_args([
        "delete",
        "--dry-run",
        "--yes",
        "--protected-subscriptions",
        "sub-a",
        "sub-b",
        "--cleanup-empty-resource-groups",
    ])

    assert args.command == "delete"
    assert args.dry_run is True
    assert args.yes is True
    assert args.config == "/tmp/exclusions.yaml"
    assert args.protected_subscriptions == ["sub-a", "sub-b"]
    assert args.cleanup_empty_resource_groups is True


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
    
    mock_resource = MagicMock()
    mock_resources = [mock_resource]
    
    # Configure the second spinner call to return resources
    mock_spinner.side_effect = spinner_results(mock_subscriptions, mock_resources)
    
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
    
    mock_spinner.side_effect = spinner_results(mock_subscriptions, [MagicMock()])
    
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
    args.cleanup_empty_resource_groups = False
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
    mock_confirmation.assert_called_once_with(
        mock_resources_to_delete,
        mock_creds_instance,
        args.dry_run,
        cleanup_empty_resource_groups=False,
    )
    mock_delete.assert_called_once_with(
        mock_creds_instance,
        mock_resources_to_delete,
        args.dry_run,
        cleanup_empty_rgs=False,
    )
    mock_completion.assert_called_once_with(True, len(mock_deleted), len(mock_failed)) 
