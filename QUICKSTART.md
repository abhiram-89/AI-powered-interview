# Quick Start Guide

Get the AI Interview Assistant running in 5 minutes!

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# Make the start script executable
chmod +x start.sh

# Start all services
./start.sh
```

This will:
- Start MongoDB on port 27017
- Start FastAPI backend on port 8000
- Start Next.js frontend on port 3000

Visit http://localhost:3000 to use the application!

## Option 2: Manual Setup

### Prerequisites
- Node.js 20+ 
- Python 3.11+
- MongoDB 7.0+

### Step 1: Install Dependencies

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or install manually:
npm install
cd backend && pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy environment templates
cp .env.example .env.local
cp backend/.env.example backend/.env

# Edit the files with your configuration
```

### Step 3: Setup Database

```bash
# Make sure MongoDB is running
# Then run:
python scripts/setup_mongodb.py
```

### Step 4: Start Development Servers

```bash
# Terminal 1: Frontend
npm run dev

# Terminal 2: Backend
cd backend
uvicorn main:app --reload
```

## Using Makefile Commands

```bash
make install    # Install dependencies
make dev        # Run both frontend and backend
make setup-db   # Initialize database
make start      # Start with Docker
make stop       # Stop Docker containers
```

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

## Default Credentials (Docker)

- **MongoDB Username**: admin
- **MongoDB Password**: password123

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process or use different ports
```

### MongoDB Connection Error
```bash
# Check MongoDB is running
docker-compose ps

# View MongoDB logs
docker-compose logs mongodb
```

### Frontend Can't Connect to Backend
- Ensure `NEXT_PUBLIC_API_URL` in `.env.local` points to http://localhost:8000
- Check backend is running: curl http://localhost:8000

## Next Steps

1. Explore the frontend at http://localhost:3000
2. Check API documentation at http://localhost:8000/docs
3. Read the full README.md for detailed information
4. Customize the interview questions in MongoDB

Need help? Check the full documentation in README.md and DEPLOYMENT.md
