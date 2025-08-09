.PHONY: help install install-dev test lint format type-check clean build dist upload upload-test install-local uninstall pre-commit-install pre-commit-run pre-commit-update validate-build wheel sdist package-check release-check install-build-deps

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install package in current environment"
	@echo "  install-dev  - Install package with dev dependencies"
	@echo "  test         - Run tests with coverage"
	@echo "  lint         - Run linting (flake8, pylint)"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  clean        - Clean build artifacts"
	@echo "  validate-build - Validate pyproject.toml and build configuration"
	@echo "  build        - Build distribution packages (wheel + sdist)"
	@echo "  wheel        - Build wheel distribution only"
	@echo "  sdist        - Build source distribution only"
	@echo "  dist         - Alias for build"
	@echo "  upload       - Upload to PyPI (requires build first)"
	@echo "  upload-test  - Upload to Test PyPI"
	@echo "  package-check- Validate package build and tests"
	@echo "  release-check- Complete release validation"
	@echo "  install-build-deps - Install build dependencies"
	@echo "  install-local- Install using install.sh script"
	@echo "  uninstall    - Uninstall using install.sh script"
	@echo "  pre-commit-install - Install pre-commit hooks"
	@echo "  pre-commit-run     - Run pre-commit on all files"
	@echo "  pre-commit-update  - Update pre-commit hooks"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Development targets
test:
	python -m pytest tests/ -v --cov=src/serverwatch_analyzer --cov-report=html --cov-report=term

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

pre-commit-update:
	pre-commit autoupdate

# Build targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

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
dev-setup: install-dev pre-commit-install
	@echo "Development environment ready!"
	@echo "Run 'make check' to verify everything works"

# Package development workflow
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
