# 🔄 Intelligent Requirements Update Workflow

## Overview

The `update-requirements` job has been optimized to act intelligently and only when needed.

## ✅ New Logic

### When does the job run?

```yaml
# Only on pull requests targeting 'develop'
github.event_name == 'pull_request' &&
github.event.pull_request.base.ref == 'develop' &&
!startsWith(github.actor, 'dependabot')
```

**Execution on:**

- ✅ Pull Request → `develop` branch
- ✅ From manual contributors
- ❌ **Not** on Dependabot PRs
- ❌ **Not** on direct pushes to `main`/`develop`

### Workflow Steps

1. **Checkout PR Source Branch**
   - Uses `github.head_ref` (PR source branch)
   - Enables write-back with `GITHUB_TOKEN`

2. **Generate requirements.txt**
   - Analyzes current dependencies in `src/`
   - Creates updated `requirements.txt`

3. **Smart Change Detection**

   ```bash
   git diff --quiet requirements.txt
   # → only commit if changes exist
   ```

4. **Conditional Commit**
   - Only on actual changes
   - Commit directly to PR source branch
   - `[skip ci]` prevents infinite loops

5. **PR Comment Notification**
   - Informs about automatic updates
   - Only on actual changes

## 🎯 Benefits

### Protection Rules Compliance

- ✅ **No direct commits** to protected branches
- ✅ **Commits to PR source branch** (allowed)
- ✅ **Normal PR review processes** remain intact

### Efficiency

- ✅ **No unnecessary commits** for unchanged requirements.txt
- ✅ **No Dependabot interference**
- ✅ **Automatic notification** on updates

### Workflow

- ✅ **Requirements always current** after PR merge
- ✅ **Visible changes** in PR diff
- ✅ **Review-friendly** - changes are part of the PR

## 📋 Example Flow

```mermaid
graph TD
    A[Developer creates PR → develop] --> B{Is target = develop?}
    B -->|Yes| C{Is actor ≠ dependabot?}
    B -->|No| Z[Job skip]
    C -->|Yes| D[Generate requirements.txt]
    C -->|No| Z
    D --> E{Did requirements.txt change?}
    E -->|Yes| F[Commit to PR branch]
    E -->|No| G[Log: No changes needed]
    F --> H[Comment in PR]
    G --> I[Workflow complete]
    H --> I
```

## 🔧 Technical Details

### Branch Strategy

```yaml
# Checkout PR source branch
ref: ${{ github.head_ref }}
# Commit back to PR branch
branch: ${{ github.head_ref }}
```

### Change Detection

```bash
if git diff --quiet requirements.txt; then
  echo "changed=false"
else
  echo "changed=true"
  git diff requirements.txt  # Show changes
fi
```

### PR Integration

- Commits appear in PR timeline
- Changes are reviewable
- Normal merge process
- Requirements automatically current after merge

## 🚀 Result

**Intelligent, protection-rule-compliant requirements management** without unnecessary commits or workflow interference!
