# pre-commit with Auto-Formatting Configuration Guide

## 📝 Automatic Corrections Activated

The `.pre-commit-config.yaml` was optimized to perform **automatic corrections**:

### 🔧 Auto-Fix Tools

| Tool             | What is corrected automatically  | Config Flag               |
| ---------------- | -------------------------------- | ------------------------- |
| **autopep8**     | Line length, indentation, spaces | `--aggressive --in-place` |
| **black**        | Code formatting, style           | `--line-length=79`        |
| **isort**        | Import sorting                   | `--profile=black`         |
| **prettier**     | YAML/JSON formatting             | Auto-Format               |
| **markdownlint** | Markdown formatting              | `--fix`                   |

### 🚀 Execution Order (Important!)

```yaml
1. isort          # Sorts imports
2. black          # Formats code
3. autopep8       # Fixes PEP8 problems (incl. line length)
4. flake8         # Checks remaining issues
5. mypy           # Type-checking
```

## ⚡ Usage

### Automatic correction before commit

```bash
# Correct all files automatically
make pre-commit-run

# Only execute certain hooks
pre-commit run black --all-files
pre-commit run autopep8 --all-files
```

### Manual corrections

```bash
# Only fix line-length problems
autopep8 --max-line-length=79 --aggressive --in-place src/**/*.py

# Black formatting
black --line-length=79 src/ tests/

# Import sorting
isort --profile=black --line-length=79 src/ tests/
```

## 🎯 Special Features

### autopep8 Configuration

```yaml
args: [--max-line-length=79, --aggressive, --aggressive, --in-place]
```

- `--max-line-length=79`: Breaks long lines
- `--aggressive`: Makes more aggressive corrections
- `--in-place`: Writes changes directly to files

### Line Length Handling

```python
# Before (too long):
raise ValueError("Custom analysis_prompt must contain {report_content} placeholder")

# After (automatically corrected):
raise ValueError(
    "Custom analysis_prompt must contain "
    "{report_content} placeholder"
)
```

## 🔄 Pre-commit Hook Installation

For automatic execution on every commit:

```bash
# Install pre-commit hooks
make dev-setup

# Or manually:
pre-commit install
```

Then all corrections will be automatically applied on every `git commit`!

## 🛠️ Troubleshooting

### Common Problems

**Problem:** Hook fails with "command not found"

```bash
# Solution: Reinstall environment
pre-commit clean
pre-commit install --install-hooks
```

**Problem:** autopep8 and black conflict

```bash
# Solution: Order is important - isort → black → autopep8
# Black runs before autopep8, so autopep8 only makes PEP8 fixes
```

**Problem:** Too aggressive changes

```bash
# Solution: Less aggressive autopep8 settings
args: [--max-line-length=79, --in-place]  # Only one --aggressive
```

## 📊 Successful Configuration

```bash
✅ trim trailing whitespace.....Passed
✅ fix end of files.............Passed
✅ check yaml..................Passed
✅ check toml..................Passed
✅ isort.......................Passed
✅ black.......................Passed
✅ autopep8....................Passed  # <- Automatic PEP8 corrections!
✅ flake8......................Passed  # <- No more errors!
✅ mypy........................Passed
```

The configuration now **automatically** corrects most formatting problems! 🎉
