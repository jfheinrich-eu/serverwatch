#!/usr/bin/env bash

echo "🚀 Setting up ServerWatch DevContainer..."

# Update system packages
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

# Setup virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "🔧 Installing dependencies in virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip

# Install from lock file if available (for exact reproducibility)
if [ -f "requirements-dev.lock" ]; then
    echo "📋 Installing from lock file for exact reproducibility..."
    pip install -r requirements-dev.lock
else
    echo "📦 Installing from pyproject.toml..."
    pip install -e ".[dev]"
fi

# Install pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Make activation script executable
chmod +x activate-dev.sh

# Set proper ownership for virtual environment
sudo chown -R vscode:vscode .venv

echo "✅ DevContainer setup complete!"
echo "Virtual environment ready at: $(pwd)/.venv"
echo "Python interpreter: $(pwd)/.venv/bin/python"
