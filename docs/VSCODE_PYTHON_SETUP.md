# VSCode Python Virtual Environment Setup Guide

## 🐍 Automatic Virtual Environment for VSCode

This project is configured to automatically use an isolated Python environment where all dependencies are installed and correctly recognized by VSCode.

## 🚀 Quick Start

### Option 1: Automatic Setup Script

```bash
# Automatically activates the virtual environment
./activate-dev.sh
```

### Option 2: Makefile (recommended)

```bash
# Complete development setup
make dev-setup
```

### Option 3: Manual

```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## ⚙️ VSCode Configuration

### Automatic Interpreter Detection

The `.vscode/settings.json` is configured for:

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true
}
```

### Activated Features

✅ **Linting:** pylint, flake8, mypy, bandit
✅ **Formatting:** black (79 characters), isort
✅ **Testing:** pytest with automatic discovery
✅ **Type Checking:** mypy with basic mode
✅ **Auto Import:** Intelligent code completion
✅ **Format on Save:** Automatic formatting when saving

## 🔍 Debugging Configuration

The `.vscode/launch.json` contains pre-configured debug configurations:

### Available Debug Modes

- **Python: Current File** - Debug the current file
- **Python: Run Tests** - Debug tests
- **Python: Run Specific Test** - Debug a specific test
- **Python: Analyzer Demo** - Debug the analyzer with API key

## 📦 Dependency Management

### Installed Packages

**Runtime Dependencies:**

- `openai>=1.99.3` - OpenAI API Client
- `markdown>=3.8.2` - Markdown processing

**Development Dependencies:**

- `pytest>=8.4.1` - Testing framework
- `pytest-cov>=6.2.1` - Coverage reporting
- `pytest-mock>=3.14.1` - Mocking utilities
- `pylint>=3.3.7` - Python linter
- `black>=25.1.0` - Code formatter
- `isort>=6.0.1` - Import sorter
- `flake8>=7.3.0` - Style guide enforcement
- `mypy>=1.17.1` - Static type checker
- `bandit>=1.8.6` - Security linter
- `pre-commit>=4.2.0` - Git hook framework

### Package Installation

```bash
# Editable installation (for development)
pip install -e ".[dev]"

# Only runtime dependencies
pip install -e .

# Only development dependencies
pip install pytest black isort flake8 mypy pylint bandit
```

## 🧪 Testing Integration

### VSCode Test Discovery

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests", "-v", "--tb=short"],
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

### Test Commands

```bash
# In terminal (with activated venv)
pytest tests/ -v

# Via VSCode Test Explorer
# - Automatic discovery of all tests
# - Run/Debug individual tests
# - Coverage integration
```

## 🔧 Development Workflow

### 1. Activate Environment

```bash
source .venv/bin/activate
# or
./activate-dev.sh
```

### 2. Write Code

- VSCode automatically recognizes the virtual environment
- IntelliSense works with all installed packages
- Auto-import suggests available modules

### 3. Format Code

```bash
# Automatically on save in VSCode
# or manually:
make format
make pre-commit-fix
```

### 4. Run Tests

```bash
# Via VSCode Test Explorer
# or terminal:
make test
pytest tests/ -v
```

### 5. Check Linting

```bash
make lint
make pre-commit-run
```

## 🔍 Troubleshooting

### Problem: VSCode doesn't recognize virtual environment

**Solution 1:** Manually select Python interpreter

1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Select `./.venv/bin/python`

**Solution 2:** Check VSCode settings

```bash
# Check .vscode/settings.json
cat .vscode/settings.json | grep defaultInterpreterPath
```

**Solution 3:** Reload VSCode window

1. `Ctrl+Shift+P` → "Developer: Reload Window"

### Problem: Module not found

**Solution:** Check editable installation

```bash
source .venv/bin/activate
pip list | grep serverwatch-analyzer
# Should show: serverwatch-analyzer 0.1.0 /workspaces/serverwatch
```

**Reinstall if necessary:**

```bash
pip install -e ".[dev]"
```

### Problem: Linting errors in VSCode

**Solution:** Check linter paths

```bash
source .venv/bin/activate
which pylint  # Should be .venv/bin/pylint
which black   # Should be .venv/bin/black
which mypy    # Should be .venv/bin/mypy
```

### Problem: Tests not recognized

**Solution 1:** Refresh test discovery

1. `Ctrl+Shift+P` → "Python: Refresh Tests"

**Solution 2:** Check pytest configuration

```bash
# pyproject.toml should contain:
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## 📁 File Structure

```bash
serverwatch/
├── .venv/                     # Virtual environment
│   ├── bin/python            # Python interpreter
│   ├── lib/python3.12/       # Installed packages
│   └── pyvenv.cfg            # venv configuration
├── .vscode/
│   ├── settings.json         # VSCode Python settings
│   └── launch.json           # Debug configurations
├── src/serverwatch_analyzer/ # Source code
├── tests/                    # Test files
├── activate-dev.sh           # Development environment script
└── pyproject.toml           # Project configuration
```

## ✅ Check Success Status

```bash
# Run all checks
source .venv/bin/activate

# 1. Python version
python --version

# 2. Virtual environment active?
echo $VIRTUAL_ENV  # Should be /workspaces/serverwatch/.venv

# 3. Package importable?
python -c "import serverwatch_analyzer; print('✅ OK')"

# 4. Dependencies available?
python -c "import openai, pytest, black; print('✅ Dependencies OK')"

# 5. VSCode integration?
code --list-extensions | grep python  # ms-python.python should be there
```

## 🎯 Best Practices

### 1. Always use virtual environment

```bash
# Before every development session:
source .venv/bin/activate
```

### 2. Manage dependencies in pyproject.toml

```toml
# Add new runtime dependency:
dependencies = ["openai>=1.99.3", "new-package>=1.0.0"]

# Add new dev dependency:
[project.optional-dependencies]
dev = ["pytest>=8.4.1", "new-dev-tool>=1.0.0"]
```

### 3. Use pre-commit hooks

```bash
# Install once:
pre-commit install

# Run automatically before each commit:
# - black (code formatting)
# - isort (import sorting)
# - flake8 (linting)
# - mypy (type checking)
# - bandit (security check)
```

### 4. Run tests regularly

```bash
# During development:
pytest tests/ --tb=short  # Quick overview

# Before commits:
make test  # Complete tests with coverage
```

## 🚀 Ready for Development

With this configuration, you have a completely isolated, reproducible Python development environment that seamlessly integrates with VSCode. All dependencies are correctly installed and VSCode automatically recognizes them for IntelliSense, debugging, and testing.
