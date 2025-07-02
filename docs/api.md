# API Reference

This document provides detailed information about Azure Nuke's internal API and modules.

## Core Modules

### Authentication (`src/auth.py`)

Handles Azure authentication and subscription management.

#### Functions

##### `get_subscriptions(credentials)`

Retrieves accessible Azure subscriptions.

**Parameters:**
- `credentials` (DefaultAzureCredential): Azure credentials object

**Returns:**
- `List[Subscription]`: List of accessible subscriptions

**Example:**
```python
from azure.identity import DefaultAzureCredential
from src.auth import get_subscriptions

credentials = DefaultAzureCredential()
subscriptions = get_subscriptions(credentials)
```

### Discovery (`src/discovery.py`)

Handles resource discovery across Azure subscriptions.

#### Functions

##### `discover_all_resources(credentials, subscriptions)`

Discovers resources across all provided subscriptions.

**Parameters:**
- `credentials` (DefaultAzureCredential): Azure credentials
- `subscriptions` (List[Subscription]): List of subscriptions to scan

**Returns:**
- `List[AzureResource]`: List of discovered resources

##### `discover_subscription_resources(credentials, subscription)`

Discovers resources in a single subscription.

**Parameters:**
- `credentials` (DefaultAzureCredential): Azure credentials
- `subscription` (Subscription): Subscription to scan

**Returns:**
- `List[AzureResource]`: List of resources in the subscription

### Filtering (`src/filtering.py`)

Applies exclusion rules to filter resources.

#### Functions

##### `load_exclusions(config_path)`

Loads exclusion configuration from YAML file.

**Parameters:**
- `config_path` (str): Path to exclusions configuration file

**Returns:**
- `Dict`: Exclusion configuration dictionary

##### `filter_resources(resources, exclusions, progress_bar=None)`

Filters resources based on exclusion rules.

**Parameters:**
- `resources` (List[AzureResource]): Resources to filter
- `exclusions` (Dict): Exclusion configuration
- `progress_bar` (Optional): Progress bar object

**Returns:**
- `Tuple[List[AzureResource], List[AzureResource]]`: Tuple of (resources_to_delete, resources_to_preserve)

### Deletion (`src/deletion.py`)

Handles resource deletion operations.

#### Functions

##### `delete_resources(credentials, resources, dry_run=False)`

Deletes or simulates deletion of resources.

**Parameters:**
- `credentials` (DefaultAzureCredential): Azure credentials
- `resources` (List[AzureResource]): Resources to delete
- `dry_run` (bool): If True, only simulate deletion

**Returns:**
- `Tuple[List[AzureResource], List[Tuple[AzureResource, str]]]`: Tuple of (deleted_resources, failed_resources)

### Safety (`src/safety.py`)

Provides safety checks and confirmation prompts.

#### Functions

##### `require_confirmation(resources, credentials, dry_run=False)`

Prompts user for confirmation before deletion.

**Parameters:**
- `resources` (List[AzureResource]): Resources to be deleted
- `credentials` (DefaultAzureCredential): Azure credentials
- `dry_run` (bool): If True, indicates dry run mode

**Returns:**
- `bool`: True if user confirms, False otherwise

##### `is_protected_subscription(subscription_id, protected_list)`

Checks if a subscription is in the protected list.

**Parameters:**
- `subscription_id` (str): Subscription ID to check
- `protected_list` (List[str]): List of protected subscription IDs

**Returns:**
- `bool`: True if subscription is protected

## Data Models

### AzureResource

Represents an Azure resource.

**Attributes:**
- `id` (str): Full Azure resource ID
- `name` (str): Resource name
- `type` (str): Resource type (e.g., "Microsoft.Storage/storageAccounts")
- `location` (str): Azure region
- `resource_group` (str): Resource group name
- `subscription_id` (str): Subscription ID
- `tags` (Dict[str, str]): Resource tags

**Example:**
```python
resource = AzureResource(
    id="/subscriptions/.../resourceGroups/rg1/providers/Microsoft.Storage/storageAccounts/storage1",
    name="storage1",
    type="Microsoft.Storage/storageAccounts",
    location="eastus",
    resource_group="rg1",
    subscription_id="12345678-1234-1234-1234-123456789abc",
    tags={"Environment": "dev"}
)
```

### Subscription

Represents an Azure subscription.

**Attributes:**
- `subscription_id` (str): Subscription ID
- `display_name` (str): Subscription display name
- `tenant_id` (str): Tenant ID
- `state` (str): Subscription state

## CLI Interface

### Command Structure

```
aznuke <command> [options]
```

### Commands

#### `scan`

Scans Azure resources without making changes.

**Options:**
- `--profile` (str): Azure profile name
- `--region` (str): Target region
- `--checks` (str): Comma-separated resource types
- `--config` (str): Configuration file path
- `--output` (str): Output format (text|json)
- `--severity` (str): Severity filter (low|medium|high)
- `--verbose` (bool): Verbose output

#### `delete`

Deletes Azure resources.

**Options:**
- `--profile` (str): Azure profile name
- `--region` (str): Target region
- `--checks` (str): Comma-separated resource types
- `--config` (str): Configuration file path
- `--dry-run` (bool): Dry run mode
- `--protected-subscriptions` (List[str]): Protected subscription IDs
- `--yes` (bool): Skip confirmation
- `--verbose` (bool): Verbose output

## Error Handling

### Exception Types

#### `AuthenticationError`

Raised when Azure authentication fails.

#### `PermissionError`

Raised when insufficient permissions are detected.

#### `ResourceNotFoundError`

Raised when a resource cannot be found.

#### `ConfigurationError`

Raised when configuration is invalid.

### Error Codes

| Code | Description |
|------|-------------|
| 1 | Authentication failure |
| 2 | Permission denied |
| 3 | Configuration error |
| 4 | Resource not found |
| 5 | Network error |

## Configuration Schema

### Exclusions Configuration

```yaml
resource_types:
  - type: array
    items: string
    description: "Azure resource types to exclude"

name_patterns:
  - type: array
    items: string
    description: "Regex patterns for resource names to exclude"

resource_ids:
  - type: array
    items: string
    description: "Specific resource IDs to exclude"

tags:
  - type: object
    additionalProperties: string
    description: "Tag key-value pairs to exclude"

regions:
  - type: array
    items: string
    description: "Azure regions to exclude"

resource_groups:
  - type: array
    items: string
    description: "Resource group names to exclude"
```

## Extension Points

### Custom Resource Handlers

You can extend Azure Nuke with custom resource handlers:

```python
from src.discovery import ResourceHandler

class CustomResourceHandler(ResourceHandler):
    def can_handle(self, resource_type):
        return resource_type == "Microsoft.Custom/resources"
    
    def discover(self, client, subscription_id):
        # Custom discovery logic
        pass
    
    def delete(self, client, resource):
        # Custom deletion logic
        pass
```

### Custom Filters

Add custom filtering logic:

```python
from src.filtering import Filter

class CustomFilter(Filter):
    def should_exclude(self, resource, exclusions):
        # Custom filtering logic
        return False
```

## Testing

### Unit Tests

Run unit tests:

```bash
pytest tests/
```

### Integration Tests

Run integration tests (requires Azure credentials):

```bash
pytest tests/integration/
```

### Coverage

Generate coverage report:

```bash
pytest --cov=src tests/
```

## Performance Considerations

### Parallel Processing

Azure Nuke uses async operations for better performance:

```python
import asyncio
from src.discovery import discover_all_resources

async def main():
    resources = await discover_all_resources(credentials, subscriptions)
```

### Rate Limiting

Azure API calls are rate-limited automatically using exponential backoff.

### Memory Usage

For large environments, consider using streaming for resource processing:

```python
for resource_batch in stream_resources(subscriptions):
    process_batch(resource_batch)
```

## Next Steps

- [Contributing](contributing.md) - How to contribute to the project
- [GitHub Repository](https://github.com/sojay/azure-nuke) - Source code and issues 