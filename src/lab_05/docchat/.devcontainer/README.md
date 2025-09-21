# DevContainer Setup for DocChat

This project includes a complete DevContainer configuration for consistent development across different environments.

## Features

- **Python 3.11** base environment
- **UV Package Manager** for fast dependency management
- **Pre-configured VS Code extensions** for Python development
- **Port forwarding** for Gradio (7860) and other services (8000)
- **Git and GitHub CLI** included
- **Linting and formatting tools** (Black, Ruff, Flake8)

## Getting Started

### Prerequisites

- Docker installed on your system
- VS Code with the "Remote - Containers" extension

### Opening the Project

1. Clone the repository
2. Open the project folder in VS Code
3. When prompted, click "Reopen in Container" or use the Command Palette:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Remote-Containers: Reopen in Container"
   - Select the option

### First Time Setup

The devcontainer will automatically:

1. Install all dependencies using UV: `uv sync --dev`
2. Set up the Python environment
3. Configure VS Code settings and extensions

### Environment Variables

Make sure to create a `.env` file in the project root with your Azure credentials:

```bash
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=your_embeddings_deployment
AZURE_OPENAI_API_VERSION=2024-02-01
```

### Running the Application

Once inside the devcontainer:

```bash
# Install/update dependencies
uv sync

# Run the main application
uv run python app.py

# Run tests
uv run pytest

# Run with specific Python command
uv run python -m your_module
```

### Available Scripts

The devcontainer includes these pre-configured tools:

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run black .`
- **Type checking**: `uv run mypy .`
- **Testing**: `uv run pytest`

### Port Forwarding

The following ports are automatically forwarded:

- **7860**: Gradio interface
- **8000**: FastAPI or other web services

You can access these at `http://localhost:7860` and `http://localhost:8000` respectively.

### UV Package Management

This project uses UV for fast Python package management:

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Update dependencies
uv sync

# Create virtual environment
uv venv

# Run commands in the environment
uv run python script.py
```

### VS Code Extensions Included

- Python language support
- Pylint, Flake8, Black formatter
- Ruff linter
- Jupyter notebook support
- JSON support
- Git integration

### Troubleshooting

1. **Container won't build**: Check Docker is running and you have enough disk space
2. **Dependencies not installing**: Try rebuilding the container (`Ctrl+Shift+P` → "Remote-Containers: Rebuild Container")
3. **Environment variables not loading**: Ensure your `.env` file is in the project root
4. **Ports not accessible**: Check VS Code port forwarding panel

### Customization

You can modify the devcontainer configuration by editing:

- `.devcontainer/devcontainer.json` - VS Code settings and extensions
- `.devcontainer/Dockerfile` - Container configuration and system packages
- `pyproject.toml` - Python dependencies and project configuration