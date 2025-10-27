#!/bin/bash

# Setup script for LLM CTF Challenge on Ubuntu
# This script will install all necessary dependencies and verify the environment

set -e  # Exit on any error

echo "=== OWASP CTF: Invisible Vector Setup Script ==="
echo "Starting installation process..."

# Check if we're running on Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "This script is designed for Ubuntu systems."
    exit 1
fi

source /etc/os-release
if [ "$ID" != "ubuntu" ]; then
    echo "This script is designed for Ubuntu systems. Detected: $ID"
    exit 1
fi

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Python and pip if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt-get install -y python3
fi

if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt-get install -y python3-pip
fi

# Install system dependencies for llama-cpp-python
echo "Installing system dependencies..."
sudo apt-get install -y build-essential python3-dev

# Check if the model file exists
MODEL_FILE="phi3-mini.Q4_K_M.gguf"
if [ ! -f "$MODEL_FILE" ]; then
    echo "ERROR: Model file '$MODEL_FILE' not found in the current directory!"
    echo "Please download the model and place it in this directory before running the setup."
    exit 1
fi

echo "Model file found: $MODEL_FILE"

# Create a virtual environment
echo "Creating Python virtual environment..."
python3 -m venv ctf-env
source ctf-env/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install flask llama-cpp-python

# Create requirements.txt for future reference
echo "Creating requirements.txt file..."
pip freeze > requirements.txt

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py not found in the current directory!"
    exit 1
fi

echo "app.py found"

# Test if the model can be loaded
echo "Testing model loading..."
python3 -c "
from llama_cpp import Llama
try:
    print('Testing model loading...')
    llm = Llama(model_path='./phi3-mini.Q4_K_M.gguf', n_ctx=4096, n_threads=4, verbose=False)
    print('Model loaded successfully!')
except Exception as e:
    print(f'Error loading model: {e}')
    exit(1)
"

echo "=== Setup Complete ==="
echo ""
echo "To start the CTF challenge:"
echo "1. Activate the virtual environment: source ctf-env/bin/activate"
echo "2. Run the application: python3 app.py"
echo "3. Open a browser and go to: http://localhost:5000"
echo ""
echo "Note: The first run might take a while as the model initializes."
