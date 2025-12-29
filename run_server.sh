#!/bin/bash

# Dog MCP Server Runner
# This script ensures the server runs with proper environment setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the server
exec python "$SCRIPT_DIR/src/server.py"
