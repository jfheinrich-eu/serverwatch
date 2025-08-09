#!/bin/bash

# 🧪 DevContainer Persistence Test Script
# Validates that the development environment is properly set up

set -e

echo "🧪 Testing DevContainer Persistence..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test functions
test_passed() {
    echo -e "${GREEN}✅ $1${NC}"
}

test_failed() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

test_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "1. 🐍 Testing Python Virtual Environment..."
if [ -d ".venv" ]; then
    test_passed "Virtual environment directory exists"
else
    test_failed "Virtual environment directory missing"
fi

if [ -f ".venv/bin/activate" ]; then
    test_passed "Virtual environment activation script found"
else
    test_failed "Virtual environment activation script missing"
fi

echo ""
echo "2. 📦 Testing Python Interpreter..."
# shellcheck source=/dev/null
source .venv/bin/activate

if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    test_passed "Python interpreter available: $PYTHON_VERSION"
else
    test_failed "Python interpreter not found in virtual environment"
fi

if [[ "$(which python)" == *".venv"* ]]; then
    test_passed "Using virtual environment Python: $(which python)"
else
    test_warning "Python interpreter not from virtual environment: $(which python)"
fi

echo ""
echo "3. 📋 Testing Package Installation..."
if pip show serverwatch-analyzer &> /dev/null; then
    test_passed "serverwatch-analyzer package installed (editable)"
else
    test_failed "serverwatch-analyzer package not installed"
fi

EXPECTED_PACKAGES=("pytest" "black" "isort" "flake8" "mypy" "bandit" "pre-commit")
for package in "${EXPECTED_PACKAGES[@]}"; do
    if pip show "$package" &> /dev/null; then
        test_passed "$package installed"
    else
        test_failed "$package not installed"
    fi
done

echo ""
echo "4. 🔧 Testing Development Tools..."
if command -v pre-commit &> /dev/null; then
    test_passed "pre-commit available"
    if pre-commit --version &> /dev/null; then
        test_passed "pre-commit is working"
    else
        test_warning "pre-commit available but not working properly"
    fi
else
    test_failed "pre-commit not available"
fi

echo ""
echo "5. 🧪 Testing Project Structure..."
if [ -f "pyproject.toml" ]; then
    test_passed "pyproject.toml found"
else
    test_failed "pyproject.toml missing"
fi

if [ -f "requirements-dev.lock" ]; then
    test_passed "requirements-dev.lock found"
    LOCK_PACKAGES=$(wc -l < requirements-dev.lock)
    test_passed "Lock file contains $LOCK_PACKAGES packages"
else
    test_failed "requirements-dev.lock missing"
fi

if [ -d "src/serverwatch_analyzer" ]; then
    test_passed "Source code directory found"
else
    test_failed "Source code directory missing"
fi

echo ""
echo "6. 🔍 Testing Import Capability..."
if python -c "import serverwatch_analyzer; print('Import successful')" &> /dev/null; then
    test_passed "serverwatch_analyzer import works"
else
    test_failed "Cannot import serverwatch_analyzer"
fi

echo ""
echo "7. ⚡ Testing Quick Commands..."
if [ -f "Makefile" ]; then
    test_passed "Makefile found"
    if make help &> /dev/null; then
        test_passed "Makefile help target works"
    else
        test_warning "Makefile help target not working"
    fi
else
    test_warning "Makefile not found"
fi

echo ""
echo "8. 📊 Environment Summary..."
echo "----------------------------------------"
echo "Python Version: $(python --version)"
echo "Python Location: $(which python)"
echo "Pip Version: $(pip --version)"
echo "Virtual Environment: $VIRTUAL_ENV"
echo "Working Directory: $(pwd)"
echo "Installed Packages: $(pip list --format=freeze | wc -l) packages"
echo "----------------------------------------"

echo ""
echo -e "${GREEN}🎉 DevContainer Persistence Test Completed!${NC}"
echo ""
echo "💡 Next steps:"
echo "   • Run 'make test' to execute unit tests"
echo "   • Run 'make lint' to check code quality"
echo "   • Run 'make dev-setup' if any issues found"
echo ""
echo "📚 For more info, see: docs/DEVCONTAINER_PERSISTENCE.md"
