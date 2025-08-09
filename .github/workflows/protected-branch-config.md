# Protected Branch Configuration Guide

This document explains how the release workflows handle protected branches.

## Branch Protection Settings

### Main Branch Protection

- **Branch:** `main`
- **Required status checks:** All CI checks must pass
- **Require pull request reviews:** At least 1 reviewer
- **Dismiss stale reviews:** Enabled
- **Require review from code owners:** Enabled
- **Restrict pushes:** Only allow merge commits from PRs

### Develop Branch Protection

- **Branch:** `develop`
- **Required status checks:** All CI checks must pass
- **Require pull request reviews:** At least 1 reviewer
- **Allow force pushes:** Disabled
- **Allow deletions:** Disabled

## Workflow Adaptations

### Release Workflow (`release.yml`)

- **Trigger:** Push to `main` branch
- **Action:** Uses `jefflinse/pr-semver-bump` which creates PRs instead of direct commits
- **Protection Compliance:** ✅ Compatible with protected branches

### Tag Workflow (`tag.yml`)

- **Trigger:** New tag creation
- **Action:** Creates PR to sync `develop` branch instead of direct commit
- **Protection Compliance:** ✅ Compatible with protected branches
- **PR Details:**
  - Base: `develop`
  - Branch: `release-sync-{run_id}`
  - Auto-deletes branch after merge

## Required Permissions

### GitHub Token Permissions

The default `GITHUB_TOKEN` needs these permissions:

```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

### Repository Settings

1. Go to Settings → Branches
2. Add protection rules for `main` and `develop`
3. Enable "Require status checks to pass before merging"
4. Add required status checks: `test`, `lint`, `build`

## Workflow Execution Flow

### Normal Release Process

1. Developer creates PR to `main`
2. CI runs all checks
3. After review approval and CI success, PR is merged
4. `release.yml` triggers and creates version bump PR
5. Version bump PR is reviewed and merged
6. Tag is created, triggering `tag.yml`
7. `tag.yml` creates sync PR to `develop`
8. Sync PR is reviewed and merged

### Emergency Hotfix Process

1. Create hotfix branch from `main`
2. Fix issue and create PR to `main`
3. Follow normal release process
4. Create additional PR from `main` to `develop` if needed

## Troubleshooting

### Common Issues

- **Workflow fails with "Branch protection rule":** Check that workflows use PR creation instead of direct commits
- **Auto-merge not working:** Ensure required status checks are configured correctly
- **Token permission errors:** Verify `GITHUB_TOKEN` has required permissions

### Manual Intervention

If automatic PR creation fails:

1. Manually create PR with the required changes
2. Reference the failed workflow run in the PR description
3. Ensure all CI checks pass before merging
