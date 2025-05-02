"""
Pytest configuration and fixtures
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the project root directory to Python's module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock fixtures for Azure services
@pytest.fixture
def mock_credentials():
    """Mock Azure credentials"""
    mock_creds = MagicMock()
    return mock_creds

@pytest.fixture
def mock_subscription():
    """Mock Azure subscription"""
    mock_sub = MagicMock()
    mock_sub.subscription_id = "00000000-0000-0000-0000-000000000000"
    mock_sub.display_name = "Test Subscription"
    return mock_sub

@pytest.fixture
def mock_resource():
    """Mock Azure resource"""
    mock_res = MagicMock()
    mock_res.id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/test-rg/providers/Microsoft.Storage/storageAccounts/teststorage"
    mock_res.name = "teststorage"
    mock_res.type = "Microsoft.Storage/storageAccounts"
    mock_res.resource_group = "test-rg"
    mock_res.tags = {"Environment": "Test"}
    return mock_res

@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file for testing"""
    config_content = """
resource_types:
  - Microsoft.KeyVault/vaults

name_patterns:
  - "^prod-.*$"
  - ".*-do-not-delete$"

resource_ids:
  - "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/important-rg/providers/Microsoft.Storage/storageAccounts/criticalaccount"

tags:
  Environment: "Production"
  DoNotDelete: "true"
"""
    config_file = tmp_path / "test_exclusions.yaml"
    config_file.write_text(config_content)
    return config_file 