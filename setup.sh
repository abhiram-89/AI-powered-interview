#!/bin/bash

echo "=========================================="
echo "AI Interview Assistant - Setup Script"
echo "=========================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed."
    echo "Please install Node.js: https://nodejs.org/"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3: https://www.python.org/"
    exit 1
fi

echo "Step 1: Installing frontend dependencies..."
npm install

echo ""
echo "Step 2: Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

echo ""
echo "Step 3: Creating environment files..."

if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "Created .env.local"
fi

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "Created backend/.env"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure environment variables in .env.local and backend/.env"
echo "2. Start MongoDB: make sure MongoDB is running"
echo "3. Setup database: python scripts/setup_mongodb.py"
echo "4. Run development: make dev"
echo ""
echo "Or use Docker: ./start.sh"
echo "=========================================="
