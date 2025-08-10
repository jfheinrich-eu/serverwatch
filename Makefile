.PHONY: help install install-dev test lint format type-check clean build dist upload upload-test install-local uninstall pre-commit-install pre-commit-run pre-commit-update validate-build wheel sdist package-check release-check install-build-deps test-python-version test-all-python-versions install-python-managers

# Default target
help:
	@echo "Available targets:"
	@echo ""
	@echo "Group: Installation and Setup"
	@echo "  install                 - Install package in current environment"
	@echo "  install-dev             - Install package with development dependencies"
	@echo "  install-build-deps      - Install build dependencies"
	@echo "  install-local           - Install using install.sh script"
	@echo "  uninstall               - Uninstall using install.sh script"
	@echo "  install-python-managers - Install Python version management tools (uv/pyenv)"
	@echo ""
	@echo "Group: Build"
	@echo "  build          - Build distribution packages (wheel + sdist)"
	@echo "  dist           - Alias for build"
	@echo "  sdist          - Build source distribution only"
	@echo "  wheel          - Build wheel distribution only"
	@echo "  validate-build - Validate pyproject.toml and build configuration"
	@echo "  package-check  - Validate package build and tests"
	@echo "  clean          - Clean build artifacts"
	@echo "  dev-setup      - Create virtual environment and setup development environment"
	@echo ""
	@echo "Group: Testing and Quality Assurance"
	@echo "  test                            - Run tests with coverage"
	@echo "  test-all-python-versions        - Test compatibility with all supported Python versions"
	@echo "  test-persist                    - Test DevContainer persistence setup"
	@echo "  test-python-version VERSION=X.Y - Test compatibility with specific Python version (auto-installs if needed)"
	@echo "  type-check                      - Run type checking with mypy"
	@echo ""
	@echo "Group: Code Quality"
	@echo "  lint         - Run linting (flake8, pylint)"
	@echo "  format       - Format code with black and isort"
	@echo ""
	@echo "Group: Pre-commit"
	@echo "  pre-commit-run     - Run pre-commit on all files"
	@echo "  pre-commit-fix     - Run auto-fixing formatters only"
	@echo "  pre-commit-install - Install pre-commit hooks"
	@echo "  pre-commit-update  - Update pre-commit hooks"
	@echo ""
	@echo "Group: Upload to PyPI"
	@echo "  upload       - Upload to PyPI (requires build first)"
	@echo "  upload-test  - Upload to Test PyPI"
	@echo ""
	@echo "Group: Release Workflow"
	@echo "  before-commit-checks - Run checks before committing"
	@echo "  release-check        - Complete release validation"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

dev-setup:
	@echo "🚀 Setting up development environment..."
	@if [ ! -d ".venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv .venv; \
	fi
	@echo "🔧 Activating virtual environment and installing dependencies..."
	@bash -c "source .venv/bin/activate && pip install --upgrade pip && pip install -e '.[dev]'"
	@echo "🪝 Installing pre-commit hooks..."
	@bash -c "source .venv/bin/activate && pre-commit install"
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "To activate: source .venv/bin/activate"
	@echo "Or run: ./activate-dev.sh"

# Development targets
test:
	python -m pytest tests/ -v --cov=src/serverwatch_analyzer --cov-branch --cov-report=html --cov-report=term --cov-report=xml --cov-report=lcov:cov.info

test-persist:
	@echo "🧪 Testing DevContainer persistence setup..."
	@./test-persistence.sh

lint:
	flake8 src/serverwatch_analyzer tests/
	pylint src/serverwatch_analyzer tests/

format:
	black src/serverwatch_analyzer tests/
	isort src/serverwatch_analyzer tests/

type-check:
	mypy src/serverwatch_analyzer

# Check all code quality tools
check: format lint type-check test

# Pre-commit targets
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

pre-commit-fix:
	@echo "🔧 Running auto-fixing formatters..."
	pre-commit run isort --all-files
	pre-commit run black --all-files
	pre-commit run autopep8 --all-files
	pre-commit run prettier --all-files
	pre-commit run markdownlint --all-files
	@echo "✅ Auto-fixes completed! Run 'make pre-commit-run' to verify."

pre-commit-update:
	pre-commit autoupdate

# Build targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .venv-test-*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f cov.info coverage.lcov coverage.xml

validate-build:
	@echo "Validating pyproject.toml..."
	python -m pip check
	python -c "import tomllib; f=open('pyproject.toml','rb'); tomllib.load(f); print('✓ pyproject.toml is valid')"
	@echo "Testing package installation..."
	python -m pip install -e . --quiet
	@echo "✓ Package can be installed successfully"

build: clean validate-build
	@echo "Building wheel and source distribution..."
	python -m build
	@echo "✓ Build completed successfully"

wheel: clean
	@echo "Building wheel distribution..."
	python -m build --wheel

sdist: clean
	@echo "Building source distribution..."
	python -m build --sdist

dist: build

upload: build
	@echo "Uploading to PyPI..."
	@echo "Note: Make sure you have configured your PyPI credentials"
	python -m twine check dist/*
	python -m twine upload dist/*

upload-test: build
	@echo "Uploading to Test PyPI..."
	python -m twine check dist/*
	python -m twine upload --repository testpypi dist/*

# System installation (requires root)
install-local:
	sudo ./install.sh

install-local-test:
	sudo RUN_TESTS=true ./install.sh

uninstall:
	sudo ./install.sh uninstall

# Development workflow
package-check: validate-build test lint type-check
	@echo "Package validation completed successfully!"

# CI/CD targets
ci: format lint type-check test
	@echo "All CI checks passed!"

# Release workflow
release-check: clean validate-build test lint type-check
	@echo "Release checks completed successfully!"
	@echo "Ready for release. Run 'make build' to create distribution packages."

# Install additional build dependencies
install-build-deps:
	python -m pip install --upgrade pip build twine

# Python version compatibility testing
test-python-version:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: Please specify Python version with VERSION=X.Y"; \
		echo "Usage: make test-python-version VERSION=3.9"; \
		echo "Available versions: 3.9, 3.10, 3.11, 3.12"; \
		exit 1; \
	fi
	@echo "Testing compatibility with Python $(VERSION)..."
	@echo "Checking if Python $(VERSION) is available..."
	@if command -v python$(VERSION) >/dev/null 2>&1; then \
		echo "✓ Python $(VERSION) found locally"; \
		PYTHON_CMD=python$(VERSION); \
	elif command -v pyenv >/dev/null 2>&1; then \
		echo "Installing Python $(VERSION) via pyenv..."; \
		pyenv install -s $(VERSION); \
		pyenv local $(VERSION); \
		PYTHON_CMD=python; \
	elif command -v uv >/dev/null 2>&1; then \
		echo "Using uv to manage Python $(VERSION)..."; \
		rm -rf .venv-test-$(VERSION); \
		uv venv .venv-test-$(VERSION) --python $(VERSION); \
		.venv-test-$(VERSION)/bin/pip install --upgrade pip; \
		.venv-test-$(VERSION)/bin/pip install -e ".[dev]"; \
		.venv-test-$(VERSION)/bin/python -c "import sys; print(f'Python version: {sys.version}')"; \
		.venv-test-$(VERSION)/bin/pytest tests/ -v; \
		.venv-test-$(VERSION)/bin/python -c "from serverwatch_analyzer import ServerAnalyzer, ReportGenerator; print('✓ Package imports successfully')"; \
		echo "✓ Python $(VERSION) compatibility test passed!"; \
		echo "Cleaning up test environment..."; \
		rm -rf .venv-test-$(VERSION); \
		exit 0; \
	else \
		echo "❌ Python $(VERSION) not found and no package manager (pyenv/uv) available"; \
		echo "Please install Python $(VERSION) manually or install pyenv/uv"; \
		exit 1; \
	fi; \
	rm -rf .venv-test-$(VERSION); \
	$$PYTHON_CMD -m venv .venv-test-$(VERSION); \
	.venv-test-$(VERSION)/bin/pip install --upgrade pip; \
	.venv-test-$(VERSION)/bin/pip install -e ".[dev]"; \
	.venv-test-$(VERSION)/bin/python -c "import sys; print(f'Python version: {sys.version}')"; \
	.venv-test-$(VERSION)/bin/pytest tests/ -v; \
	.venv-test-$(VERSION)/bin/python -c "from serverwatch_analyzer import ServerAnalyzer, ReportGenerator; print('✓ Package imports successfully')"; \
	echo "✓ Python $(VERSION) compatibility test passed!"; \
	echo "Cleaning up test environment..."; \
	rm -rf .venv-test-$(VERSION)

# Test all supported Python versions with auto-installation
test-all-python-versions:
	@echo "Testing all supported Python versions with auto-installation..."
	$(MAKE) test-python-version VERSION=3.9
	$(MAKE) test-python-version VERSION=3.10
	$(MAKE) test-python-version VERSION=3.11
	$(MAKE) test-python-version VERSION=3.12
	@echo "✅ All Python versions tested successfully!"

# Install Python version management tools
install-python-managers:
	@echo "Installing Python version management tools..."
	@if ! command -v pyenv >/dev/null 2>&1 && ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv (fast Python package manager)..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "✓ uv installed. Restart your shell or run: source ~/.bashrc"; \
	else \
		echo "✓ Python manager already available"; \
	fi

# Run this rule before commit your work
before-commit-checks: pre-commit-run lint test
