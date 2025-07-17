# Release Workflow

## Branch Strategy

- **`main`**: Production releases only (triggers PyPI publishing)
- **`staging`**: Development work, docs updates, non-version changes
- **Feature branches**: For specific features, merge to staging first

## When to Create New Versions

### Version Bump Required ✅
- **Code changes** that affect functionality
- **Dependency updates** 
- **Bug fixes** that change behavior
- **New features** or commands
- **Configuration changes** that affect users

### No Version Bump Needed ❌
- **Documentation updates** (README, docs/, *.md files)
- **CI/CD workflow changes** (.github/workflows/)
- **Development tooling** (linting, testing setup)
- **Comments and formatting** changes
- **Homebrew formula development notes**

## Release Process

### For Documentation/Non-Code Changes
```bash
# Work on staging branch
git checkout staging
# Make changes
git add . && git commit -m "docs: update installation guide"
git push origin staging

# Merge to main when ready
git checkout main
git merge staging
git push origin main
```

### For Version Releases
```bash
# Work on staging branch
git checkout staging
# Make code changes
git add . && git commit -m "feat: add new scan filters"

# Test thoroughly on staging
# When ready for release:
git checkout main
git merge staging

# Create version tag (triggers CI/CD)
git tag v0.1.X
git push origin main --tags

# Update Homebrew formula
# 1. Update URL and SHA256 in homebrew/aznuke.rb
# 2. Update version in formula
# 3. Copy to tap repository
```

## CI/CD Triggers

- **Tags matching `v*`**: Triggers PyPI publishing + GitHub release
- **Push to main**: Triggers documentation deployment
- **Push to staging**: No publishing, only tests

## Homebrew Updates

Only update Homebrew formula after:
1. ✅ Tag is created
2. ✅ PyPI publishing succeeds  
3. ✅ GitHub release is created

## Version Numbering

- **Patch** (0.1.X): Bug fixes, minor improvements
- **Minor** (0.X.0): New features, major improvements  
- **Major** (X.0.0): Breaking changes, major refactoring

## Quick Reference

```bash
# Documentation update (no version)
git checkout staging → edit docs → commit → merge to main

# Code change (version required)  
git checkout staging → edit code → commit → merge to main → git tag v0.1.X → push tags

# Homebrew update (after successful release)
Update formula → copy to tap → test installation
``` 