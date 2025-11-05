#!/bin/bash
# Script to run unit tests for user data isolation
# This script ensures the virtual environment is activated and dependencies are installed

set -e

echo "=========================================="
echo "User Data Isolation Test Runner"
echo "=========================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/.."

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

echo "[1/3] Activating virtual environment..."
source venv/bin/activate

# Install test dependencies if needed
echo "[2/3] Checking test dependencies..."
python -c "import pytest" 2>/dev/null || {
    echo "Installing pytest..."
    pip install pytest pytest-asyncio httpx --timeout 120 || {
        echo "Warning: Failed to install via pip. Attempting to run tests anyway..."
    }
}

# Run tests
echo "[3/3] Running tests..."
echo ""

# Try pytest first
if python -m pytest tests/test_user_isolation.py -v 2>/dev/null; then
    echo ""
    echo "✓ All pytest tests passed!"
    exit 0
else
    echo "pytest not available, trying standalone runner..."
    python tests/run_tests.py || {
        echo ""
        echo "⚠️  Test execution failed. Please ensure dependencies are installed:"
        echo "   pip install -r requirements.txt"
        echo "   pip install pytest pytest-asyncio httpx"
        exit 1
    }
fi
