# CI/CD Setup Guide

This guide explains how to set up the required tokens and secrets for Azure Nuke's CI/CD pipeline.

## Required Secrets

### 1. GH_PAT (GitHub Personal Access Token)

**Purpose**: Used by the homebrew workflow to push updates to the homebrew tap repository.

**Required Permissions**:
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

**Setup Steps**:

1. **Generate Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token" → "Generate new token (classic)"
   - Set expiration (recommend 1 year)
   - Select scopes:
     - ✅ `repo` - Full control of private repositories
     - ✅ `workflow` - Update GitHub Action workflows
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)

2. **Add to Repository**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GH_PAT`
   - Value: Paste your personal access token
   - Click "Add secret"

### 2. PYPI_API_TOKEN (PyPI API Token)

**Purpose**: Used to publish packages to PyPI.

**Setup Steps**:

1. **Generate Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens)
   - Click "Add API token"
   - Token name: `azure-nuke-ci`
   - Scope: Select your project or "Entire account"
   - Click "Create token"
   - **Copy the token immediately**

2. **Add to Repository**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI API token
   - Click "Add secret"

## CI/CD Workflows

### Build and Release Workflow

**File**: `.github/workflows/build.yml`

**Triggers**:
- Push to tags (`v*`)
- Pull requests to main branch
- Manual dispatch

**Jobs**:
1. **Build**: Creates cross-platform binaries for Linux, macOS, and Windows
2. **PyPI**: Publishes Python package to PyPI
3. **Release**: Creates GitHub release with binary attachments

### Homebrew Formula Update

**File**: `.github/workflows/homebrew.yml`

**Triggers**:
- Release published

**Requirements**:
- `GH_PAT` secret with repo permissions
- Homebrew tap repository: `sojay/homebrew-tap`

## Troubleshooting

### Common Issues

#### 1. HTTP 403 Error in Homebrew Workflow

**Error**: `HTTP 403` when accessing release tarball

**Cause**: Missing or invalid `GH_PAT` token

**Solution**:
1. Check if `GH_PAT` secret exists in repository settings
2. Verify token has `repo` and `workflow` permissions
3. Ensure token hasn't expired
4. Regenerate token if necessary

#### 2. PyPI Upload Failed - File Already Exists

**Error**: `File already exists` when uploading to PyPI

**Cause**: Version number already published

**Solution**:
1. Increment version number
2. Create new git tag
3. Push tag to trigger new release

#### 3. Version Detection Issues

**Error**: setuptools_scm detects wrong version

**Cause**: Git tag not properly associated with commit

**Solution**:
1. Ensure git history is fetched: `fetch-depth: 0`
2. Check tag placement: `git tag --points-at HEAD`
3. Use version override system in workflow

### Debug Commands

```bash
# Check current version detection
python -c "import setuptools_scm; print(setuptools_scm.get_version())"

# Check git tags
git tag --points-at HEAD
git tag -l | sort -V

# Check package version
python -c "import aznuke; print(aznuke.__version__)"
```

## Security Best Practices

1. **Token Rotation**: Regularly rotate personal access tokens
2. **Minimal Permissions**: Only grant necessary permissions
3. **Separate Tokens**: Use different tokens for different purposes
4. **Monitor Usage**: Check token usage in GitHub settings
5. **Revoke Unused**: Remove tokens that are no longer needed

## Repository Structure

```
.github/
├── workflows/
│   ├── build.yml          # Main CI/CD pipeline
│   └── homebrew.yml       # Homebrew formula updates
├── CODEOWNERS            # Code review assignments
└── dependabot.yml        # Dependency updates

homebrew/
└── aznuke.rb             # Homebrew formula template
```

## Workflow Status

You can monitor workflow status at:
- Actions tab in your GitHub repository
- Workflow badges in README.md
- GitHub notifications for failures 