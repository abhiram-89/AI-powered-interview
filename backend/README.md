# AI Interview Assistant - Backend API

FastAPI backend for conducting AI-powered technical interviews with MongoDB database.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup MongoDB:
```bash
# Run MongoDB setup script
python ../scripts/setup_mongodb.py
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your MongoDB connection string
```

4. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
- `GET /` - Check API status

### Interviews
- `POST /api/interviews` - Create new interview
- `GET /api/interviews` - List all interviews
- `GET /api/interviews/{id}` - Get interview details
- `GET /api/interviews/{id}/question` - Get next question
- `POST /api/interviews/{id}/response` - Submit answer
- `POST /api/interviews/{id}/complete` - Complete interview
- `GET /api/interviews/{id}/evaluation` - Get evaluation results

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
