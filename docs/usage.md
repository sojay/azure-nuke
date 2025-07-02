# Usage

Azure Nuke provides two main commands: `scan` and `delete`. This guide covers all available options and common use cases.

## Commands Overview

### Scan Command

The `scan` command identifies Azure resources according to specified criteria without making any changes.

```bash
aznuke scan [OPTIONS]
```

### Delete Command

The `delete` command removes Azure resources based on the same criteria as scan.

```bash
aznuke delete [OPTIONS]
```

## Global Options

These options are available for both commands:

| Option | Description | Example |
|--------|-------------|---------|
| `--profile` | Azure subscription profile name | `--profile production` |
| `--region` | Azure region to target | `--region westus2` |
| `--checks` | Comma-separated list of resource types | `--checks storage,vm` |
| `--config` | Path to exclusions configuration file | `--config custom.yaml` |
| `-v, --verbose` | Enable verbose output | `-v` |

## Scan Options

Additional options specific to the scan command:

| Option | Description | Example |
|--------|-------------|---------|
| `--output` | Output format (text or json) | `--output json` |
| `--severity` | Filter by severity level | `--severity high` |

## Delete Options

Additional options specific to the delete command:

| Option | Description | Example |
|--------|-------------|---------|
| `--dry-run` | Preview without deleting | `--dry-run` |
| `--protected-subscriptions` | List of protected subscription IDs | `--protected-subscriptions sub1 sub2` |
| `--yes, -y` | Skip confirmation prompt | `--yes` |

## Common Use Cases

### 1. Full Environment Scan

Scan all resources across all accessible subscriptions:

```bash
aznuke scan
```

### 2. Targeted Scanning

Scan specific resource types in a particular region:

```bash
aznuke scan --checks storage,virtualmachines --region eastus
```

### 3. Export Scan Results

Export scan results as JSON for further processing:

```bash
aznuke scan --output json > azure_resources.json
```

### 4. Dry Run Deletion

Preview what would be deleted without actually deleting:

```bash
aznuke delete --dry-run
```

### 5. Automated Deletion

Delete resources without confirmation (use with caution):

```bash
aznuke delete --yes
```

### 6. Protected Subscriptions

Exclude specific subscriptions from deletion:

```bash
aznuke delete --protected-subscriptions "sub-id-1" "sub-id-2"
```

## Resource Types

Azure Nuke supports the following resource types:

### Storage
- `Microsoft.Storage/storageAccounts`
- `Microsoft.Storage/storageAccounts/blobServices`
- `Microsoft.Storage/storageAccounts/fileServices`

### Compute
- `Microsoft.Compute/virtualMachines`
- `Microsoft.Compute/disks`
- `Microsoft.Compute/snapshots`
- `Microsoft.Compute/images`

### Network
- `Microsoft.Network/virtualNetworks`
- `Microsoft.Network/publicIPAddresses`
- `Microsoft.Network/networkSecurityGroups`
- `Microsoft.Network/loadBalancers`

### Key Vault
- `Microsoft.KeyVault/vaults`

### Monitor
- `Microsoft.Monitor/actionGroups`
- `Microsoft.Monitor/alertRules`

## Output Formats

### Text Output (Default)

```
[SCANNING] Starting resource discovery...
Found 150 total resources
[SELECTED] 25 resources for deletion
[EXCLUDED] 125 resources based on filters

Resources Selected for Deletion:
├── Microsoft.Storage/storageAccounts (5)
├── Microsoft.Compute/virtualMachines (10)
└── Microsoft.Network/publicIPAddresses (10)
```

### JSON Output

```json
{
  "total_resources": 150,
  "selected_for_deletion": 25,
  "excluded": 125,
  "resources": [
    {
      "id": "/subscriptions/.../resourceGroups/rg1/providers/Microsoft.Storage/storageAccounts/storage1",
      "name": "storage1",
      "type": "Microsoft.Storage/storageAccounts",
      "location": "eastus",
      "tags": {},
      "resource_group": "rg1"
    }
  ]
}
```

## Error Handling

Azure Nuke handles various error conditions gracefully:

- **Authentication failures**: Clear error messages with authentication guidance
- **Permission errors**: Identifies resources that can't be accessed
- **Network issues**: Retries with exponential backoff
- **Resource locks**: Skips locked resources with warnings

## Best Practices

### 1. Always Start with Dry Run

```bash
# First, see what would be deleted
aznuke delete --dry-run

# Then proceed with actual deletion
aznuke delete
```

### 2. Use Exclusions Configuration

Create a comprehensive exclusions file to protect critical resources:

```bash
aznuke scan --config production-exclusions.yaml
```

### 3. Target Specific Resources

Be specific about what you want to clean up:

```bash
# Clean up only storage accounts in development environment
aznuke delete --checks storage --region eastus2
```

### 4. Monitor and Log

Use verbose mode for detailed logging:

```bash
aznuke delete --verbose > deletion.log 2>&1
```

## Troubleshooting

### Common Issues

**Issue**: "No subscriptions found"
**Solution**: Ensure Azure authentication is properly configured with `az login`

**Issue**: "Permission denied"
**Solution**: Verify your account has the necessary permissions (Contributor or Owner)

**Issue**: "Resource not found"
**Solution**: Resource may have been deleted by another process; re-run the scan

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
aznuke scan --verbose
```

## Next Steps

- [Configuration](configuration.md) - Set up exclusions and preferences
- [API Reference](api.md) - Technical details and advanced usage 