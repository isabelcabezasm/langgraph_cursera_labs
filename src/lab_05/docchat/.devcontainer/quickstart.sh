#!/bin/bash

# DocChat DevContainer Quick Start Script

echo "🚀 Setting up DocChat development environment..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f "template.env" ]; then
        cp template.env .env
        echo "✅ Created .env from template. Please update with your Azure credentials."
    else
        echo "❌ No template.env found. Please create .env file manually."
    fi
fi

# Install/update dependencies
echo "📦 Installing dependencies with UV..."
uv sync --dev

# Verify Python environment
echo "🐍 Python version:"
uv run python --version

# Check Azure dependencies
echo "☁️  Checking Azure AI packages..."
uv run python -c "
try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.core.credentials import AzureKeyCredential
    print('✅ Azure AI packages are available')
except ImportError as e:
    print(f'❌ Azure AI packages error: {e}')
"

# Show next steps
echo ""
echo "🎉 DevContainer setup complete!"
echo ""
echo "Next steps:"
echo "1. Update your .env file with Azure credentials"
echo "2. Run the application: uv run python app.py"
echo "3. Run tests: uv run pytest integration_tests/"
echo "4. Access Gradio UI at http://localhost:7860"
echo ""
echo "Available UV commands:"
echo "  uv run python app.py          # Run the main application"
echo "  uv run pytest                 # Run tests"
echo "  uv run black .                # Format code"
echo "  uv run ruff check .           # Lint code"
echo "  uv add package-name           # Add new dependency"
echo ""