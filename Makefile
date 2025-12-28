.PHONY: help install dev build start stop clean setup-db

help:
	@echo "AI Interview Assistant - Available Commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make dev         - Run development servers"
	@echo "  make build       - Build production bundles"
	@echo "  make start       - Start with Docker Compose"
	@echo "  make stop        - Stop Docker containers"
	@echo "  make setup-db    - Initialize MongoDB database"
	@echo "  make clean       - Clean build artifacts"

install:
	@echo "Installing frontend dependencies..."
	npm install
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

dev:
	@echo "Starting development servers..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@make -j 2 dev-frontend dev-backend

dev-frontend:
	npm run dev

dev-backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

build:
	@echo "Building frontend..."
	npm run build
	@echo "Build complete!"

start:
	@echo "Starting with Docker Compose..."
	docker-compose up -d
	@echo "Services running:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend: http://localhost:8000"
	@echo "  MongoDB: localhost:27017"

stop:
	@echo "Stopping Docker containers..."
	docker-compose down

setup-db:
	@echo "Setting up MongoDB database..."
	python scripts/setup_mongodb.py
	@echo "Database setup complete!"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf .next
	rm -rf node_modules
	rm -rf backend/__pycache__
	@echo "Clean complete!"

logs:
	docker-compose logs -f

restart:
	@make stop
	@make start
