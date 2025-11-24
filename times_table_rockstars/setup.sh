#!/bin/bash

# Setup script for Times Table Rockstars
# This script helps set up the development environment

echo "🎸 Times Table Rockstars - Setup Script 🎸"
echo "==========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
pip install -r requirements.txt

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python main.py"
echo ""
echo "For iOS deployment: See DEPLOYMENT.md"
echo "For Android deployment: See DEPLOYMENT.md"
echo ""
echo "Happy coding! 🎸"
