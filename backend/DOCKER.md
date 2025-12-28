# Docker Deployment

Run the entire stack with Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed
- Docker Compose v2.0+

## Quick Start

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: interview_mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongodb_data:/data/db
    networks:
      - interview_network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: interview_backend
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://admin:password123@mongodb:27017/ai_interview_assistant?authSource=admin
      API_HOST: 0.0.0.0
      API_PORT: 8000
      CORS_ORIGINS: http://localhost:3000
    depends_on:
      - mongodb
    networks:
      - interview_network

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: interview_frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
    networks:
      - interview_network

volumes:
  mongodb_data:

networks:
  interview_network:
    driver: bridge
```

## Dockerfile (Backend)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Dockerfile (Frontend)

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
```

## Initialize Database

```bash
# After services are running
docker-compose exec backend python ../scripts/setup_mongodb.py
```

## Access Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MongoDB: localhost:27017

## Production Build

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d
