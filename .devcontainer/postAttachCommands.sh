#!/bin/bash

curl https://pyenv.run | bash

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

pip3 install --user pipreqs pytest flake8 auto8
pip3 install --user --upgrade openai
