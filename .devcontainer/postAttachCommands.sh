#!/bin/bash

echo "🔗 Attaching to ServerWatch DevContainer..."

# Setup pyenv (keeping existing functionality)
if [ ! -d "$HOME/.pyenv" ]; then
    echo "📦 Installing pyenv..."
    curl https://pyenv.run | bash
fi

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Install some global Python tools
pip3 install --user pipreqs pytest flake8 auto8
pip3 install --user --upgrade openai

# Ensure virtual environment is available
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    echo "✅ Virtual environment found at .venv/"
    echo "To activate: source .venv/bin/activate"
    echo "Or run: ./activate-dev.sh"
else
    echo "⚠️  Virtual environment not found. Run 'make dev-setup' to create it."
fi

# Show helpful information
echo ""
echo "🎯 Development commands:"
echo "  make dev-setup      - Setup/rebuild virtual environment"
echo "  source .venv/bin/activate - Activate virtual environment"
echo "  ./activate-dev.sh   - Auto-activate with status check"
echo "  make test          - Run tests"
echo "  make lint          - Run linting"
echo "  make pre-commit-run - Run all pre-commit checks"
