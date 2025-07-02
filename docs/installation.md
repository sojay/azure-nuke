# Installation

Azure Nuke can be installed using several methods depending on your preferences and platform.

## Homebrew (Recommended for macOS/Linux)

### Prerequisites

- macOS 10.14+ or Linux
- [Homebrew](https://brew.sh/) installed

### Install

```bash
# Add the tap
brew tap sojay/tap

# Install Azure Nuke
brew install aznuke
```

### Update

```bash
brew update
brew upgrade aznuke
```

## Python Package (pip)

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install

```bash
pip install aznuke
```

### Update

```bash
pip install --upgrade aznuke
```

## Binary Download

Download pre-built binaries for your platform from [GitHub Releases](https://github.com/sojay/azure-nuke/releases).

### Supported Platforms

| Platform | Architecture | Binary Name |
|----------|-------------|-------------|
| Linux | AMD64 | `aznuke-linux-x64` |
| Linux | ARM64 | `aznuke-linux-arm64` |
| macOS | AMD64 | `aznuke-darwin-x64` |
| macOS | ARM64 | `aznuke-darwin-arm64` |
| Windows | AMD64 | `aznuke-windows-x64.exe` |

### Installation Steps

1. Download the appropriate binary for your platform
2. Make it executable (Linux/macOS):
   ```bash
   chmod +x aznuke-*
   ```
3. Move to your PATH:
   ```bash
   # Linux/macOS
   sudo mv aznuke-* /usr/local/bin/aznuke
   
   # Windows - Move to a directory in your PATH
   ```

## Development Installation

For development or contributing:

```bash
# Clone the repository
git clone https://github.com/sojay/azure-nuke.git
cd azure-nuke

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Verification

Verify your installation:

```bash
aznuke --version
```

## Azure Authentication

Azure Nuke uses Azure's default authentication chain. Set up authentication using one of these methods:

### Azure CLI

```bash
az login
```

### Service Principal

```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

### Managed Identity

If running on Azure resources, managed identity will be used automatically.

## Next Steps

- [Usage Guide](usage.md) - Learn how to use Azure Nuke
- [Configuration](configuration.md) - Set up exclusions and preferences 