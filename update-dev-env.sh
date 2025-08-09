#!/bin/bash

# Update Development Environment Script
# This script updates the lock file when dependencies change

echo "🔄 Updating development environment..."

# Ensure virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

# Update dependencies from pyproject.toml
echo "📦 Updating dependencies from pyproject.toml..."
pip install --upgrade pip
pip install -e ".[dev]"

# Create new lock file
echo "🔒 Creating new lock file..."
pip freeze > requirements-dev.lock

# Show what was updated
echo "✅ Update complete!"
echo "📋 Lock file updated with $(wc -l < requirements-dev.lock) packages"

# Commit the lock file if this is a git repository
if [ -d ".git" ]; then
    echo "📝 Commit the updated lock file:"
    echo "    git add requirements-dev.lock"
    echo "    git commit -m 'chore: update development dependencies lock file'"
fi
