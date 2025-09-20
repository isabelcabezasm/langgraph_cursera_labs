#!/bin/bash

# Post-create script for LangGraph Agent DevContainer
# This script runs after the container is created

echo "Installing system dependencies..."
sudo apt-get update && sudo apt-get install -y curl

echo "Installing Azure CLI..."
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

echo "Installing Python packages..."

pip install \
    langchain_openai==0.2.0 \
    langchain==0.3.23 \
    langgraph==0.2.32 \
    joblib==1.4.2 \
    azure-identity \
    pydantic \
    python-dotenv \
    langchain_community==0.3.21  \
    pygraphviz==1.14 \
    azure-cognitiveservices-search-websearch==2.0.1

# Install Jupyter kernel so notebooks in this workspace can run
if command -v python3 >/dev/null 2>&1; then
  echo "Installing ipykernel and registering Jupyter kernel..."
  python3 -m pip install --upgrade pip ipykernel || true
else
  echo "python3 not found; skipping Jupyter kernel setup."
fi

echo "Setup complete! Azure CLI and Python packages installed."

