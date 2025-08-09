# Contributing to ServerWatch Analyzer

First off, thank you for considering contributing to ServerWatch Analyzer! It's people like you that make this project great.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if applicable**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `develop`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/serverwatch.git
   cd serverwatch
   ```

3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Create a branch for your feature:

   ```bash
   git checkout -b feature/amazing-feature
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests

# Lint with flake8
flake8 src tests

# Type checking with mypy
mypy src

# Security analysis with bandit
bandit -r src
```

### Pre-commit Hooks

We recommend using pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Run against all files
pre-commit run --all-files
```

## Style Guidelines

### Python Style Guide

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep line length to 79 characters
- Use descriptive variable names

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Pull Request Labels

Please add appropriate labels to your pull requests:

- `major release`: Breaking changes
- `minor release`: New features (backwards compatible)
- `patch release`: Bug fixes (backwards compatible)
- `documentation change`: Documentation only changes
- `dependencies`: Dependency updates
- `skip-release`: Changes that don't require a release

## Testing

### Test Structure

- Unit tests in `tests/`
- Test files should be named `test_*.py`
- Test classes should be named `Test*`
- Test functions should be named `test_*`

### Writing Tests

```python
import pytest
from serverwatch_analyzer import ServerAnalyzer

def test_analyzer_initialization():
    """Test that analyzer initializes correctly."""
    analyzer = ServerAnalyzer()
    assert analyzer is not None

def test_analyze_report_with_valid_input():
    """Test report analysis with valid input."""
    analyzer = ServerAnalyzer()
    # Test implementation here
    pass
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update CHANGELOG.md for notable changes
- Include examples for new features

## Release Process

1. All changes must be made via pull requests
2. Pull requests must have appropriate labels for semantic versioning
3. Pull requests must include release notes
4. Releases are automated via GitHub Actions when merged to `main`

## Questions?

Feel free to open an issue or start a discussion if you have any questions about contributing!

Thank you for your contributions! 🎉
