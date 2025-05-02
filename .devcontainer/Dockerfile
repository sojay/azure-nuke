FROM mcr.microsoft.com/devcontainers/base:alpine

# Install core packages
RUN apk add --no-cache \
    age bash bind-tools ca-certificates curl direnv fish fzf \
    git jq moreutils openssh-client openssl python3 py3-pip \
    build-base python3-dev libffi-dev openssl-dev && \
    # Add edge repositories
    echo "@edge https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "@edge-testing https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    # Install edge packages
    apk add --no-cache lsd@edge sops@edge

# Python setup
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    black flake8 pylint pytest \
    azure-identity azure-mgmt-resource azure-cli \
    pyyaml cryptography && \
    ln -sf /opt/venv/bin/black /usr/local/bin/black && \
    ln -sf /opt/venv/bin/flake8 /usr/local/bin/flake8 && \
    ln -sf /opt/venv/bin/pylint /usr/local/bin/pylint && \
    ln -sf /opt/venv/bin/pytest /usr/local/bin/pytest && \
    ln -sf /opt/venv/bin/az /usr/local/bin/az

# Direct installation of Starship
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes

# Fish shell setup
RUN mkdir -p /home/vscode/.config/fish/conf.d /home/vscode/.config/fish/functions && \
    chown -R vscode:vscode /home/vscode/.config

# Fish hooks for direnv and starship
RUN echo "if status is-interactive" > /home/vscode/.config/fish/conf.d/hooks.fish && \
    echo "    direnv hook fish | source" >> /home/vscode/.config/fish/conf.d/hooks.fish && \
    echo "    starship init fish | source" >> /home/vscode/.config/fish/conf.d/hooks.fish && \
    echo "end" >> /home/vscode/.config/fish/conf.d/hooks.fish

# Direnv configuration
RUN mkdir -p /home/vscode/.config/direnv && \
    echo '[whitelist]' > /home/vscode/.config/direnv/direnv.toml && \
    echo 'prefix = [ "/workspaces" ]' >> /home/vscode/.config/direnv/direnv.toml && \
    chown -R vscode:vscode /home/vscode/.config