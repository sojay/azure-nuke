"""
Tests for the animations module
"""
import pytest
import asyncio
import time
from unittest.mock import MagicMock, patch, AsyncMock

from aznuke.src.animations import (
    clear_screen,
    show_startup_animation,
    async_spinner,
    print_resource_action,
    create_progress_bar,
    show_summary_by_type,
    show_completion_animation
)

@patch('os.system')
def test_clear_screen(mock_system):
    """Test clear screen functionality"""
    clear_screen()
    mock_system.assert_called_once()

@patch('aznuke.src.animations.clear_screen')
@patch('aznuke.src.animations.Figlet')
@patch('builtins.print')
@patch('time.sleep')
def test_show_startup_animation(mock_sleep, mock_print, mock_figlet, mock_clear_screen):
    """Test the startup animation display"""
    # Configure mock figlet
    mock_figlet_instance = MagicMock()
    mock_figlet.return_value = mock_figlet_instance
    mock_figlet_instance.renderText.return_value = "Azure Nuke"
    
    # Call the function
    show_startup_animation()
    
    # Verify the calls
    mock_clear_screen.assert_called_once()
    mock_figlet.assert_called_once_with(font='slant')
    mock_figlet_instance.renderText.assert_called_once_with('Azure Nuke')
    assert mock_sleep.call_count == 5
    assert mock_print.call_count > 0

@pytest.mark.asyncio
@patch('builtins.print')
async def test_async_spinner(mock_print):
    """Test the async spinner with coroutine"""
    # Create a simple coroutine that returns a value
    async def mock_coro():
        await asyncio.sleep(0.1)
        return "test_result"
    
    # Call the function
    result = await async_spinner("Testing spinner", mock_coro())
    
    # Verify the result and function behavior
    assert result == "test_result"
    mock_print.assert_called_once()

@pytest.mark.asyncio
@patch('builtins.print')
async def test_async_spinner_silent(mock_print):
    """Test the async spinner with silent mode"""
    # Create a simple coroutine that returns a value
    async def mock_coro():
        await asyncio.sleep(0.1)
        return "test_result"
    
    # Call the function in silent mode
    result = await async_spinner("Testing spinner", mock_coro(), silent=True)
    
    # Verify the result and function behavior
    assert result == "test_result"
    mock_print.assert_not_called()

@patch('builtins.print')
def test_print_resource_action_scanning(mock_print):
    """Test printing a scanning action for a resource"""
    # Create a mock resource
    mock_resource = MagicMock()
    mock_resource.name = "teststorage"
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    
    # Call the function
    print_resource_action(mock_resource, "scanning")
    
    # Verify the function behavior
    mock_print.assert_called_once()

@patch('builtins.print')
def test_print_resource_action_deleting(mock_print):
    """Test printing a deleting action for a resource"""
    # Create a mock resource
    mock_resource = MagicMock()
    mock_resource.name = "teststorage"
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    
    # Call the function
    print_resource_action(mock_resource, "deleting")
    
    # Verify the function behavior
    mock_print.assert_called_once()

@patch('builtins.print')
def test_print_resource_action_dry_run(mock_print):
    """Test printing a deleting action in dry run mode"""
    # Create a mock resource
    mock_resource = MagicMock()
    mock_resource.name = "teststorage"
    mock_resource.type = "Microsoft.Storage/storageAccounts"
    
    # Call the function in dry run mode
    print_resource_action(mock_resource, "deleting", dry_run=True)
    
    # Verify the function behavior
    mock_print.assert_called_once()

@patch('aznuke.src.animations.tqdm')
def test_create_progress_bar(mock_tqdm):
    """Test creating a progress bar"""
    # Configure the mock
    mock_progress_bar = MagicMock()
    mock_tqdm.return_value = mock_progress_bar
    
    # Call the function
    progress_bar = create_progress_bar(100, "Testing")
    
    # Verify the function behavior
    assert progress_bar == mock_progress_bar
    mock_tqdm.assert_called_once_with(total=100, desc="Testing", bar_format='{l_bar}{bar:30}{r_bar}')

@patch('builtins.print')
def test_show_summary_by_type(mock_print):
    """Test showing a summary of resources by type"""
    # Create mock resources
    mock_resource1 = MagicMock()
    mock_resource1.name = "teststorage1"
    mock_resource1.subscription_name = "Development"
    
    mock_resource2 = MagicMock()
    mock_resource2.name = "teststorage2"
    mock_resource2.subscription_name = "Development"
    
    # Create a dictionary of resources by type
    resources_by_type = {
        "Microsoft.Storage/storageAccounts": [mock_resource1, mock_resource2]
    }
    
    # Call the function
    show_summary_by_type(resources_by_type)
    
    # Verify the function behavior
    assert mock_print.call_count >= 3  # At least 3 print calls (type header, two resources)

@patch('builtins.print')
@patch('aznuke.src.animations.Figlet')
def test_show_completion_animation_success(mock_figlet, mock_print):
    """Test showing the completion animation for successful operation"""
    # Configure mock figlet
    mock_figlet_instance = MagicMock()
    mock_figlet.return_value = mock_figlet_instance
    mock_figlet_instance.renderText.return_value = "Complete!"
    
    # Call the function for successful operation
    show_completion_animation(True, 10, 0)
    
    # Verify the function behavior
    mock_figlet.assert_called_once_with(font='slant')
    mock_figlet_instance.renderText.assert_called_once_with('Complete!')
    assert mock_print.call_count >= 4

@patch('builtins.print')
@patch('aznuke.src.animations.Figlet')
def test_show_completion_animation_with_errors(mock_figlet, mock_print):
    """Test showing the completion animation with errors"""
    # Configure mock figlet
    mock_figlet_instance = MagicMock()
    mock_figlet.return_value = mock_figlet_instance
    mock_figlet_instance.renderText.return_value = "Completed"
    
    # Call the function with errors
    show_completion_animation(False, 8, 2)
    
    # Verify the function behavior
    mock_figlet.assert_called_once_with(font='slant')
    mock_figlet_instance.renderText.assert_called_once_with('Completed')
    assert mock_print.call_count >= 4 