#!/usr/bin/env bash
set -eo pipefail

# Setup fisher plugin manager for fish and install plugins
/usr/bin/fish -c "
curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher
fisher install decors/fish-colored-man
fisher install edc/bass
fisher install jorgebucaran/autopair.fish
fisher install nickeb96/puffer-fish
fisher install PatrickF1/fzf.fish
"

# Create/update virtual environment
if ! grep -q "venv /workspaces/" .venv/pyvenv.cfg; then
    rm -rf .venv
fi


# Project Python setup
python3 -m venv .venv
source .venv/bin/activate
[ -f requirements.txt ] && pip install -r requirements.txt

echo "🚀 Environment ready!"