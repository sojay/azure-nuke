# Configuration

Azure Nuke uses YAML configuration files to define exclusions and protect critical infrastructure from accidental deletion.

## Configuration File

The default configuration file is located at `config/exclusions.yaml`, but you can specify a custom path using the `--config` option.

## Exclusion Types

### 1. Resource Types

Exclude entire resource types from scanning and deletion:

```yaml
resource_types:
  - Microsoft.KeyVault/vaults
  - Microsoft.Storage/storageAccounts
  - Microsoft.Compute/virtualMachines
```

### 2. Name Patterns

Exclude resources with names matching specific patterns (regex supported):

```yaml
name_patterns:
  - "^prod-.*$"              # Resources starting with "prod-"
  - ".*-production$"         # Resources ending with "-production"
  - "^backup-.*-\d{8}$"      # Backup resources with date pattern
  - ".*-do-not-delete$"      # Resources explicitly marked
```

### 3. Resource IDs

Exclude specific resources by their full Azure Resource ID:

```yaml
resource_ids:
  - "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/critical-rg/providers/Microsoft.Storage/storageAccounts/criticaldata"
  - "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/prod-vm-01"
```

### 4. Tags

Exclude resources with specific tags:

```yaml
tags:
  Environment: "Production"
  DoNotDelete: "true"
  Owner: "Platform Team"
  Backup: "Required"
```

### 5. Regions

Exclude resources in specific Azure regions:

```yaml
regions:
  - "westus2"
  - "eastus"
  - "northeurope"
```

### 6. Resource Groups

Exclude entire resource groups:

```yaml
resource_groups:
  - "prod-rg"
  - "shared-services"
  - "network-rg"
```

## Complete Configuration Example

```yaml
# Azure Nuke Exclusions Configuration

# Exclude specific resource types
resource_types:
  - Microsoft.KeyVault/vaults
  - Microsoft.Storage/storageAccounts
  - Microsoft.Sql/servers

# Exclude resources with specific name patterns
name_patterns:
  - "^prod-.*$"
  - ".*-production$"
  - ".*-prod-.*$"
  - "backup-.*"
  - ".*-do-not-delete$"
  - "shared-.*"

# Exclude specific resource IDs
resource_ids:
  - "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/critical-rg/providers/Microsoft.Storage/storageAccounts/criticaldata"

# Exclude resources with specific tags
tags:
  Environment: "Production"
  DoNotDelete: "true"
  Owner: "Platform Team"
  Backup: "Required"
  CostCenter: "shared"

# Exclude resources in specific regions
regions:
  - "westus2"
  - "eastus"

# Exclude entire resource groups
resource_groups:
  - "prod-rg"
  - "shared-services-rg"
  - "network-rg"
  - "security-rg"
```

## Environment-Specific Configurations

### Production Environment

```yaml
# production-exclusions.yaml
resource_types:
  - Microsoft.KeyVault/vaults
  - Microsoft.Storage/storageAccounts
  - Microsoft.Sql/servers
  - Microsoft.Compute/virtualMachines

name_patterns:
  - "^prod-.*$"
  - ".*-production$"
  - ".*-prod-.*$"

tags:
  Environment: "Production"
  DoNotDelete: "true"
```

### Development Environment

```yaml
# dev-exclusions.yaml
name_patterns:
  - ".*-shared-.*$"
  - ".*-persistent-.*$"

tags:
  Persistent: "true"
  Shared: "true"
```

### Testing Environment

```yaml
# test-exclusions.yaml
name_patterns:
  - ".*-baseline-.*$"
  - ".*-template-.*$"

tags:
  Template: "true"
  Baseline: "true"
```

## Using Custom Configurations

### Command Line

```bash
# Use a custom configuration file
aznuke scan --config /path/to/custom-exclusions.yaml

# Use environment-specific configuration
aznuke delete --config configs/production.yaml --dry-run
```

### Multiple Configurations

You can maintain different configuration files for different purposes:

```
configs/
├── production.yaml
├── development.yaml
├── testing.yaml
└── shared.yaml
```

## Best Practices

### 1. Start Conservative

Begin with broad exclusions and gradually narrow them down:

```yaml
# Start with this
resource_types:
  - Microsoft.KeyVault/vaults
  - Microsoft.Storage/storageAccounts
  - Microsoft.Sql/servers

# Then add specific patterns
name_patterns:
  - "^prod-.*$"
  - ".*-production$"
```

### 2. Use Meaningful Tags

Implement a consistent tagging strategy:

```yaml
tags:
  Environment: "Production"
  DoNotDelete: "true"
  Owner: "team-name"
  Project: "project-name"
  CostCenter: "department"
```

### 3. Document Your Exclusions

Add comments to explain exclusion rules:

```yaml
# Exclude all production resources
name_patterns:
  - "^prod-.*$"        # Production resources prefix
  - ".*-production$"   # Production resources suffix

# Exclude shared infrastructure
resource_groups:
  - "shared-services"  # Shared services used by multiple teams
  - "network-rg"       # Core network infrastructure
```

### 4. Regular Review

Periodically review and update your exclusions:

- Remove exclusions for resources that no longer exist
- Add new patterns for new naming conventions
- Update tags as your tagging strategy evolves

## Validation

### Test Your Configuration

Always test your configuration with dry-run mode:

```bash
# Test the configuration
aznuke delete --config my-exclusions.yaml --dry-run
```

### Verify Exclusions

Check that your exclusions are working correctly:

```bash
# Scan with verbose output to see what's being excluded
aznuke scan --config my-exclusions.yaml --verbose
```

## Configuration Schema

The configuration file follows this schema:

```yaml
resource_types:          # Array of Azure resource types
  - string
  
name_patterns:           # Array of regex patterns
  - string
  
resource_ids:           # Array of full Azure resource IDs
  - string
  
tags:                   # Key-value pairs of tags
  key: value
  
regions:                # Array of Azure region names
  - string
  
resource_groups:        # Array of resource group names
  - string
```

## Next Steps

- [API Reference](api.md) - Technical details and advanced usage
- [Contributing](contributing.md) - How to contribute to the project 