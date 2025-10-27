#!/bin/bash

# This script automates the setup of the LLM CTF Challenge environment on Ubuntu 22.04 LTS.
# It ensures all dependencies and required files are in place before execution.

# --- Configuration ---
# You can change this directory if you like
APP_DIR="/home/ubuntu/llm_ctf_challenge"

# --- Pre-flight Checks ---
echo "[+] Checking for required files (app.py, requirements.txt)..."
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    echo "[-] ERROR: Missing required files!"
    echo "[-] Please make sure 'app.py' and 'requirements.txt' are in the same directory as this script before running."
    exit 1
fi
echo "[+] All required application files found."

# --- Step 1: System Update and Initial Setup ---
echo "[+] Updating and upgrading system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# --- Step 2: Install Python and Build Tools ---
echo "[+] Installing Python, PIP, venv, wget, and build-essential..."
sudo apt-get install python3 python3-pip python3-venv build-essential wget -y

# --- Step 3: Create Application Directory and Move Files ---
echo "[+] Creating application directory at $APP_DIR..."
mkdir -p $APP_DIR
echo "[+] Moving application files into the directory..."
mv app.py requirements.txt $APP_DIR
cd $APP_DIR

# --- Step 4: Set up Python Virtual Environment ---
echo "[+] Creating Python virtual environment..."
python3 -m venv venv

# --- Step 5: Install Python Dependencies ---
echo "[+] Installing Python dependencies from requirements.txt into the virtual environment..."
# We call pip from within the venv directly to avoid activation issues in the script
./venv/bin/pip install -r requirements.txt

# --- Step 6: Download the LLM Model ---
# Check if the model already exists to avoid re-downloading
if [ -f "phi3-mini.Q4_K_M.gguf" ]; then
    echo "[+] LLM model 'phi3-mini.Q4_K_M.gguf' already exists. Skipping download."
else
    echo "[+] Downloading the Phi-3-mini GGUF model (this may take a few minutes)..."
    wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-Q4_K_M.gguf -O phi3-mini.Q4_K_M.gguf
fi


# --- Final Instructions ---
echo ""
echo "================================================================"
echo "✅ Setup Complete!"
echo "================================================================"
echo "Your CTF environment is ready in: $APP_DIR"
echo ""
echo "To run the application:"
echo "1. Change into the directory: cd $APP_DIR"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the server: python3 app.py"
echo ""


