# API Documentation

Complete API reference for the AI Interview Assistant backend.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/`

Check if the API is online.

**Response**
```json
{
  "message": "AI Interview Assistant API",
  "status": "online",
  "version": "1.0.0"
}
```

---

### Create Interview

**POST** `/api/interviews`

Create a new interview session.

**Request Body**
```json
{
  "candidate_name": "John Doe",
  "candidate_email": "john@example.com",
  "role": "Frontend Developer",
  "experience_level": "Mid-level",
  "skills": ["React", "TypeScript", "CSS"],
  "duration": 30
}
```

**Response**
```json
{
  "interview_id": "507f1f77bcf86cd799439011",
  "message": "Interview created successfully",
  "candidate_name": "John Doe",
  "role": "Frontend Developer"
}
```

---

### Get Interview

**GET** `/api/interviews/{interview_id}`

Retrieve interview details.

**Parameters**
- `interview_id` (path): Interview ID

**Response**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "candidate_name": "John Doe",
  "candidate_email": "john@example.com",
  "role": "Frontend Developer",
  "experience_level": "Mid-level",
  "skills": ["React", "TypeScript"],
  "status": "active",
  "current_question": 3,
  "total_questions": 8,
  "created_at": "2024-01-15T10:00:00Z"
}
```

---

### Get Next Question

**GET** `/api/interviews/{interview_id}/question`

Get the next interview question.

**Parameters**
- `interview_id` (path): Interview ID

**Response**
```json
{
  "completed": false,
  "question_id": "507f191e810c19729de860ea",
  "question": "Explain the difference between controlled and uncontrolled components in React.",
  "question_number": 3,
  "total_questions": 8
}
```

**When Complete**
```json
{
  "completed": true,
  "message": "Interview completed",
  "total_questions": 8
}
```

---

### Submit Response

**POST** `/api/interviews/{interview_id}/response`

Submit an answer to a question.

**Parameters**
- `interview_id` (path): Interview ID

**Request Body**
```json
{
  "interview_id": "507f1f77bcf86cd799439011",
  "question_id": "507f191e810c19729de860ea",
  "answer": "Controlled components have their state managed by React..."
}
```

**Response**
```json
{
  "message": "Response saved successfully",
  "interview_id": "507f1f77bcf86cd799439011"
}
```

---

### Complete Interview

**POST** `/api/interviews/{interview_id}/complete`

Mark interview as complete and generate evaluation.

**Parameters**
- `interview_id` (path): Interview ID

**Response**
```json
{
  "interview_id": "507f1f77bcf86cd799439011",
  "candidate_name": "John Doe",
  "candidate_email": "john@example.com",
  "role": "Frontend Developer",
  "overall_score": 82.5,
  "scores": {
    "technical": 85.0,
    "clarity": 80.0,
    "problem_solving": 82.5
  },
  "recommendation": "Hire",
  "recommendation_color": "blue",
  "strengths": [
    "Strong technical knowledge demonstrated",
    "Clear communication skills"
  ],
  "improvements": [
    "Could provide more detailed examples"
  ],
  "total_questions": 8,
  "answered_questions": 8
}
```

---

### Get Evaluation

**GET** `/api/interviews/{interview_id}/evaluation`

Retrieve evaluation results.

**Parameters**
- `interview_id` (path): Interview ID

**Response**
```json
{
  "interview_id": "507f1f77bcf86cd799439011",
  "overall_score": 82.5,
  "scores": {
    "technical": 85.0,
    "clarity": 80.0,
    "problem_solving": 82.5
  },
  "recommendation": "Hire",
  "strengths": ["..."],
  "improvements": ["..."]
}
```

---

### List Interviews

**GET** `/api/interviews`

List all interviews with pagination.

**Query Parameters**
- `limit` (optional): Number of results (default: 10)
- `skip` (optional): Number to skip (default: 0)

**Response**
```json
{
  "interviews": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "candidate_name": "John Doe",
      "role": "Frontend Developer",
      "status": "completed",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 45,
  "limit": 10,
  "skip": 0
}
```

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "detail": "Invalid interview ID"
}
```

**404 Not Found**
```json
{
  "detail": "Interview not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test all endpoints directly.
