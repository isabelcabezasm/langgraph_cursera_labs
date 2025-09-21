FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    wget \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install UV (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    # Check where UV was installed and make it available globally
    (test -f /root/.cargo/bin/uv && cp /root/.cargo/bin/uv /usr/local/bin/uv) || \
    (test -f /root/.local/bin/uv && cp /root/.local/bin/uv /usr/local/bin/uv) || \
    (which uv && cp $(which uv) /usr/local/bin/uv) || \
    # If UV installation failed, install via pip as fallback
    pip install uv && \
    chmod +x /usr/local/bin/uv

ENV PATH="/usr/local/bin:$PATH"

# Set the working directory and fix ownership
WORKDIR /workspaces/cursera_labs/src/lab_05/docchat

# Copy the pyproject.toml file (no need for requirements.txt)
COPY pyproject.toml .

# Change ownership of workspace to vscode user
RUN chown -R $USERNAME:$USERNAME /workspaces

# Switch to the non-root user
USER $USERNAME

# Set environment variables for UV
ENV UV_SYSTEM_PYTHON=1
ENV UV_CACHE_DIR=/tmp/uv-cache

# Install dependencies using UV and pyproject.toml with flexible resolution
RUN uv sync --resolution=highest || \
    (echo "Flexible UV sync failed, trying without dev dependencies..." && \
     uv sync --no-dev --resolution=highest) || \
    (echo "UV sync failed completely, falling back to pip..." && \
     uv pip install --system -e .)

# Create UV lock file and install dependencies
RUN uv sync

# Expose ports for Gradio and other services
EXPOSE 7860 8000

# Set the default command
CMD ["bash"]