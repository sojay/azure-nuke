"""
Tests for the filtering module
"""
import os
import pytest
from unittest.mock import MagicMock, patch
import yaml

# Import the module to test
from aznuke.src.filtering import find_config_file, load_exclusions, should_preserve, filter_resources


def test_find_config_file_exists(tmp_path):
    """Test finding config file when it exists at the exact path"""
    # Create a temporary config file
    config_file = tmp_path / "exclusions.yaml"
    config_file.write_text("test content")
    
    # Find the config file using its exact path
    found_path = find_config_file(str(config_file))
    
    # Verify the path is found and matches the input path
    assert found_path == str(config_file)


def test_load_exclusions(temp_config_file):
    """Test loading exclusion rules from a YAML file"""
    # Load the exclusion rules from the temporary config file
    exclusions = load_exclusions(str(temp_config_file))
    
    # Verify the exclusion rules are loaded correctly
    assert "resource_types" in exclusions
    assert "name_patterns" in exclusions
    assert "resource_ids" in exclusions
    assert "tags" in exclusions
    assert "Microsoft.KeyVault/vaults" in exclusions["resource_types"]
    assert "^prod-.*$" in exclusions["name_patterns"]


def test_should_preserve_resource_type(mock_resource):
    """Test resource preservation based on resource type"""
    # Configure exclusions for resource type
    exclusions = {
        "resource_types": ["Microsoft.Storage/storageAccounts"]
    }
    
    # Check if the resource should be preserved
    assert should_preserve(mock_resource, exclusions)


def test_should_preserve_name_pattern(mock_resource):
    """Test resource preservation based on name pattern"""
    # Configure exclusions for name pattern
    exclusions = {
        "name_patterns": ["^test.*$"]
    }
    
    # Check if the resource should be preserved
    assert should_preserve(mock_resource, exclusions)


def test_should_preserve_resource_id(mock_resource):
    """Test resource preservation based on resource ID"""
    # Configure exclusions for resource ID
    exclusions = {
        "resource_ids": [
            "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/test-rg/providers/Microsoft.Storage/storageAccounts/teststorage"
        ]
    }
    
    # Check if the resource should be preserved
    assert should_preserve(mock_resource, exclusions)


def test_should_preserve_tags(mock_resource):
    """Test resource preservation based on tags"""
    # Configure exclusions for tags
    exclusions = {
        "tags": {
            "Environment": "Test"
        }
    }
    
    # Check if the resource should be preserved
    assert should_preserve(mock_resource, exclusions)


def test_should_not_preserve(mock_resource):
    """Test resource not preserved when no exclusion rules match"""
    # Configure exclusions that don't match the resource
    exclusions = {
        "resource_types": ["Microsoft.KeyVault/vaults"],
        "name_patterns": ["^prod-.*$"],
        "resource_ids": [
            "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/important-rg/providers/Microsoft.Storage/storageAccounts/criticalaccount"
        ],
        "tags": {
            "Environment": "Production"
        }
    }
    
    # Check if the resource should not be preserved
    assert not should_preserve(mock_resource, exclusions)


def test_filter_resources(mock_resource):
    """Test filtering resources based on exclusion rules"""
    # Create a list of resources
    resources = [mock_resource]
    
    # Configure exclusions that don't match the resource
    exclusions = {
        "resource_types": ["Microsoft.KeyVault/vaults"]
    }
    
    # Filter the resources
    resources_to_delete, resources_to_preserve = filter_resources(resources, exclusions)
    
    # Verify the resources are filtered correctly
    assert len(resources_to_delete) == 1
    assert len(resources_to_preserve) == 0


def test_filter_resources_with_progress_bar(mock_resource):
    """Test filtering resources with a progress bar"""
    # Create a list of resources
    resources = [mock_resource]
    
    # Create a mock progress bar
    progress_bar = MagicMock()
    
    # Configure exclusions that don't match the resource
    exclusions = {
        "resource_types": ["Microsoft.KeyVault/vaults"]
    }
    
    # Filter the resources with a progress bar
    filter_resources(resources, exclusions, progress_bar)
    
    # Verify the progress bar was updated
    progress_bar.update.assert_called_once_with(1) 