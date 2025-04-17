#!/bin/bash
set -e

# Set working directory (adjust if needed)
WORKDIR="$(pwd)"
BREW_DIR="$WORKDIR/homebrew"
BREW_BIN="$BREW_DIR/bin/brew"
BLENDER_PATH="$BREW_DIR/bin/blender"
PYTHON_PATH="$(which python3)"  # use existing system Python

# Step 1: Clone and set up Homebrew locally if not already present
if [ ! -d "$BREW_DIR" ]; then
  echo "Cloning Homebrew..."
  git clone https://github.com/Homebrew/brew "$BREW_DIR"
fi

# Step 2: Use the local Homebrew to install Blender
echo "Installing Blender via local Homebrew..."
"$BREW_BIN" install blender

# Step 3: Patch usdz_exporter.py to use full Blender path
echo "Patching usdz_exporter.py..."
sed -i.bak "s|blender_executable = .*|blender_executable = \"$BLENDER_PATH\"|" usdz_exporter.py

# Step 4: Start your Python backend server
echo "Launching server..."
"$PYTHON_PATH" app.py
