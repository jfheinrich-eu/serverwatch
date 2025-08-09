#!/bin/bash

# ServerWatch Development Environment Activation Script
# This script activates the virtual environment and sets up the development environment

echo "🚀 Activating ServerWatch Development Environment..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv .venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
# shellcheck source=/dev/null
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import serverwatch_analyzer" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -e ".[dev]"
    echo "✅ Dependencies installed."
fi

# Verify installation
echo "🔍 Verifying installation..."
python -c "
import sys
import serverwatch_analyzer
print(f'✅ Python: {sys.version}')
print(f'✅ Virtual Environment: {sys.prefix}')
print(f'✅ ServerWatch Analyzer: {serverwatch_analyzer.__version__}')
print(f'✅ Package location: {serverwatch_analyzer.__file__}')
"

# Setup pre-commit hooks if not already installed
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed."
fi

echo ""
echo "🎉 Development environment ready!"
echo ""
echo "Available commands:"
echo "  make test           - Run tests"
echo "  make lint           - Run linting"
echo "  make format         - Format code"
echo "  make pre-commit-run - Run all pre-commit checks"
echo "  make pre-commit-fix - Auto-fix formatting issues"
echo ""
echo "To deactivate: deactivate"
