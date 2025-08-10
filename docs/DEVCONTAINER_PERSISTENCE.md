# DevContainer Persistence Strategy

## 🔄 Automatic Rebuild on Container Restart

Your setup will be **automatically restored on every DevContainer rebuild**!

## 🛠️ What happens during Container rebuild?

### 1. PostCreateCommand (.devcontainer/postCreateCommands.sh)

```bash
# Runs once after container creation
1. Install system packages (python3-venv, python3-pip)
2. Create virtual environment (.venv/)
3. Install dependencies (from requirements-dev.lock)
4. Install pre-commit hooks
5. Set permissions
```

### 2. PostAttachCommand (.devcontainer/postAttachCommands.sh)

```bash
# Runs on every attach/reconnect
1. PyEnv setup (if desired)
2. Check virtual environment status
3. Display helpful commands
```

### 3. VSCode Settings

```json
// Automatically integrated in devcontainer.json:
- Python Interpreter: ./.venv/bin/python
- Linting: pylint, flake8, mypy, bandit
- Formatting: black, isort
- Testing: pytest
- Auto-Format on Save
```

## 📋 Lock File Strategy

### Exact Reproducibility

```bash
# requirements-dev.lock contains exact versions:
annotated-types==0.7.0
anyio==4.10.0
astroid==3.3.11
bandit==1.8.6
# ... (58 packages total)
```

### Update Workflow

```bash
# Update dependencies:
./update-dev-env.sh

# Or manually:
source .venv/bin/activate
pip install -e ".[dev]"
pip freeze > requirements-dev.lock
git add requirements-dev.lock
git commit -m "chore: update dev dependencies"
```

## 🚀 Automation in Detail

### Container Build Flow

```bash
1. DevContainer starts
   ↓
2. Execute postCreateCommands.sh
   ↓
3. Create .venv/
   ↓
4. Install requirements-dev.lock
   ↓
5. Activate VSCode settings
   ↓
6. ✅ Development environment ready!
```

### Rebuild-safe Files

- ✅ `pyproject.toml` - Project configuration
- ✅ `requirements-dev.lock` - Exact dependency versions
- ✅ `.devcontainer/devcontainer.json` - Container configuration
- ✅ `.devcontainer/postCreateCommands.sh` - Setup script
- ✅ `.vscode/settings.json` - VSCode configuration (also in devcontainer.json)
- ✅ `activate-dev.sh` - Activation script
- ✅ `update-dev-env.sh` - Update script

### What gets recreated

- 🔄 `.venv/` - Virtual environment (but identically reproduced)
- 🔄 Installed packages (but exact versions from lock file)

## 🎯 Testing Persistence

### Test rebuild

```bash
# 1. Document current state
source .venv/bin/activate
python -c "import sys; print(f'Python: {sys.version}')"
pip list

# 2. Container rebuild
Cmd+Shift+P → "Dev Containers: Rebuild Container"

# 3. Check after rebuild
source .venv/bin/activate  # Should work immediately
python -c "import serverwatch_analyzer; print('✅ Package available')"
make test  # Should run all tests
```

## 🔧 Manual Recovery

If something goes wrong:

```bash
# Recreate virtual environment
rm -rf .venv
make dev-setup

# Or completely:
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.lock
pre-commit install
```

## 🌟 Benefits of this Strategy

✅ **Automatic:** No manual setup after rebuild
✅ **Reproducible:** Exact versions via lock file
✅ **Fast:** Cached dependencies, only reinstall on changes
✅ **Consistent:** Same environment for all developers
✅ **Versioned:** Lock file in Git repository
✅ **VSCode Integration:** Settings automatically applied

## 📈 Best Practices

### 1. Keep lock file current

```bash
# After dependency changes:
./update-dev-env.sh
git add requirements-dev.lock
git commit -m "chore: update dependencies"
```

### 2. Rebuild on major changes

```bash
# After major pyproject.toml changes:
Cmd+Shift+P → "Dev Containers: Rebuild Container"
```

### 3. Validate environment

```bash
# After rebuild check:
source .venv/bin/activate
make test
make lint
```

## 🚨 Troubleshooting

### Problem: Virtual environment missing after rebuild

```bash
# Solution: Run setup again
make dev-setup
```

### Problem: Dependencies outdated

```bash
# Solution: Update lock file
./update-dev-env.sh
```

### Problem: VSCode doesn't recognize Python

```bash
# Solution: Reselect interpreter
Cmd+Shift+P → "Python: Select Interpreter" → ./.venv/bin/python
```

## ✅ Status: Fully automated

Your setup survives every container rebuild and will be identically restored! 🎉
