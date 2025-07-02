# Contributing

Thank you for your interest in contributing to Azure Nuke! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Azure CLI (for testing)
- An Azure account with appropriate permissions

### Development Setup

1. **Fork the Repository**
   
   Fork the repository on GitHub and clone your fork:
   ```bash
   git clone https://github.com/your-username/azure-nuke.git
   cd azure-nuke
   ```

2. **Set Up Development Environment**
   
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Install Development Dependencies**
   
   ```bash
   pip install pytest pytest-cov black pylint flake8
   ```

4. **Verify Installation**
   
   ```bash
   aznuke --version
   pytest tests/
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run linting
black src/ tests/
pylint src/
flake8 src/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black default)
- **Import Organization**: Use `isort` for import sorting
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Use type hints for all public functions

### Code Formatting

We use Black for code formatting:

```bash
black src/ tests/
```

### Linting

We use pylint and flake8:

```bash
pylint src/
flake8 src/
```

### Example Code Style

```python
from typing import List, Optional, Dict, Any
import asyncio
from azure.identity import DefaultAzureCredential


class ResourceHandler:
    """Handles Azure resource operations.
    
    This class provides methods for discovering and managing Azure resources
    across different subscriptions and resource types.
    
    Attributes:
        credentials: Azure credentials for authentication
        subscriptions: List of subscriptions to operate on
    """
    
    def __init__(self, credentials: DefaultAzureCredential) -> None:
        """Initialize the ResourceHandler.
        
        Args:
            credentials: Azure credentials object
        """
        self.credentials = credentials
        self.subscriptions: List[str] = []
    
    async def discover_resources(
        self, 
        subscription_id: str,
        resource_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Discover resources in a subscription.
        
        Args:
            subscription_id: The subscription ID to scan
            resource_types: Optional list of resource types to filter
            
        Returns:
            List of discovered resources
            
        Raises:
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions
        """
        # Implementation here
        pass
```

## Testing

### Unit Tests

Write unit tests for all new functionality:

```python
import pytest
from unittest.mock import Mock, patch
from src.discovery import discover_all_resources


class TestResourceDiscovery:
    """Test cases for resource discovery functionality."""
    
    @pytest.fixture
    def mock_credentials(self):
        """Mock Azure credentials."""
        return Mock()
    
    @pytest.fixture
    def mock_subscriptions(self):
        """Mock subscription list."""
        return [
            Mock(subscription_id="sub1", display_name="Subscription 1"),
            Mock(subscription_id="sub2", display_name="Subscription 2")
        ]
    
    @patch('src.discovery.ResourceManagementClient')
    async def test_discover_all_resources(
        self, 
        mock_client, 
        mock_credentials, 
        mock_subscriptions
    ):
        """Test discovering resources across subscriptions."""
        # Arrange
        mock_client.return_value.resources.list.return_value = []
        
        # Act
        resources = await discover_all_resources(mock_credentials, mock_subscriptions)
        
        # Assert
        assert isinstance(resources, list)
        assert len(resources) == 0
```

### Integration Tests

For features that interact with Azure APIs:

```python
import pytest
from azure.identity import DefaultAzureCredential
from src.auth import get_subscriptions


@pytest.mark.integration
class TestAzureIntegration:
    """Integration tests requiring Azure credentials."""
    
    @pytest.fixture(scope="class")
    def credentials(self):
        """Real Azure credentials for integration testing."""
        return DefaultAzureCredential()
    
    async def test_get_subscriptions_real(self, credentials):
        """Test getting real subscriptions."""
        subscriptions = await get_subscriptions(credentials)
        assert len(subscriptions) > 0
```

### Test Configuration

Create `pytest.ini` for test configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    integration: marks tests as integration tests (deselect with '-m "not integration"')
    slow: marks tests as slow (deselect with '-m "not slow"')
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def filter_resources(resources: List[AzureResource], exclusions: Dict[str, Any]) -> Tuple[List[AzureResource], List[AzureResource]]:
    """Filter resources based on exclusion rules.
    
    This function applies various exclusion rules to determine which resources
    should be preserved vs deleted.
    
    Args:
        resources: List of Azure resources to filter
        exclusions: Dictionary containing exclusion rules
        
    Returns:
        A tuple containing:
            - List of resources to delete
            - List of resources to preserve
            
    Raises:
        ConfigurationError: If exclusion rules are invalid
        
    Example:
        >>> exclusions = {"resource_types": ["Microsoft.Storage/storageAccounts"]}
        >>> to_delete, to_preserve = filter_resources(resources, exclusions)
    """
```

### README Updates

Update the README.md if your changes affect:
- Installation instructions
- Usage examples
- Feature descriptions
- Configuration options

### Documentation Site

Update the documentation site in the `docs/` directory:
- Add new pages for major features
- Update existing pages for changes
- Add code examples and tutorials

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Use a descriptive title with conventional commit format
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for test additions/changes

2. **Description**: Include:
   - What changes were made
   - Why the changes were needed
   - Any breaking changes
   - Testing instructions

3. **Checklist**:
   - [ ] Tests pass
   - [ ] Code is formatted (Black)
   - [ ] Linting passes
   - [ ] Documentation updated
   - [ ] Changelog updated (if applicable)

### Example Pull Request

```markdown
# feat: Add support for Azure SQL Database resource type

## Description
This PR adds support for discovering and deleting Azure SQL Database resources.

## Changes
- Added SQL Database resource handler in `src/discovery.py`
- Added SQL Database deletion logic in `src/deletion.py`
- Added unit tests for new functionality
- Updated documentation

## Testing
- All existing tests pass
- New unit tests added and passing
- Tested with real Azure SQL Database resources

## Breaking Changes
None

## Checklist
- [x] Tests pass
- [x] Code is formatted
- [x] Linting passes
- [x] Documentation updated
```

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Changelog

Update `CHANGELOG.md` with your changes:

```markdown
## [Unreleased]

### Added
- Support for Azure SQL Database resources

### Changed
- Improved error handling for authentication failures

### Fixed
- Fixed issue with resource group filtering
```

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

### Recognition

Contributors will be recognized in:
- GitHub contributors list
- CHANGELOG.md
- Documentation credits

## Development Tips

### Debugging

Use the verbose flag for debugging:

```bash
aznuke scan --verbose
```

### Testing with Real Azure Resources

For testing, create a separate Azure subscription with test resources:

```bash
# Set up test environment
export AZURE_SUBSCRIPTION_ID="your-test-subscription-id"
aznuke scan --dry-run
```

### Performance Testing

For performance testing with large resource sets:

```python
import time
from src.discovery import discover_all_resources

start_time = time.time()
resources = await discover_all_resources(credentials, subscriptions)
end_time = time.time()
print(f"Discovered {len(resources)} resources in {end_time - start_time:.2f} seconds")
```

## Thank You

Thank you for contributing to Azure Nuke! Your contributions help make cloud resource management safer and more efficient for everyone. 