# AI Interview Assistant - Developer Guide

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                │
│  ├── app/setup/page.tsx          (Interview Setup) │
│  ├── app/interview/page.tsx      (Chat Interface)  │
│  ├── app/results/page.tsx        (Results Display) │
│  └── lib/api.ts                  (API Client)      │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP/REST
                  ▼
┌─────────────────────────────────────────────────────┐
│              Backend (FastAPI)                      │
│  ├── Interview Management                          │
│  ├── Question Generation                           │
│  ├── Response Submission                           │
│  ├── AI Evaluation (NEW)                           │
│  └── Report Generation (NEW)                       │
└─────────────────┬───────────────────────────────────┘
                  │ MongoDB Protocol
                  ▼
┌─────────────────────────────────────────────────────┐
│           MongoDB Dual Database                     │
│  ├── ai_interview_assistant                        │
│  │   ├── interviews (interview data)              │
│  │   ├── questions (question bank)                │
│  │   ├── responses (user answers)                 │
│  │   └── evaluations (simple eval)                │
│  └── ai_interviews (NEW)                          │
│      └── reports (comprehensive reports)          │
└─────────────────────────────────────────────────────┘
```

## Key Classes & Services

### AIEvaluationService
**Location**: `backend/main.py`

```python
class AIEvaluationService:
    @staticmethod
    async def evaluate_answer(
        question: str,
        answer: str,
        role: str,
        skills: List[str]
    ) -> Dict[str, Any]
```

**Evaluation Factors:**
1. Answer length (50+ chars preferred)
2. Technical keywords (role-specific)
3. Structure (multiple sentences)
4. Examples (specific projects/scenarios)

**Output:**
```python
{
    "marks": int,              # 4-10
    "max_marks": 10,
    "percentage": float,       # 0-100
    "feedback": str,
    "correctness": str         # excellent|good|fair|poor
}
```

### Data Models

**QuestionEvaluation**
```python
class QuestionEvaluation(BaseModel):
    question_id: str
    question: str
    answer: str
    marks: int
    max_marks: int = 10
    percentage: float
    feedback: str
    correctness: str
```

**InterviewReport**
```python
class InterviewReport(BaseModel):
    interview_id: str
    candidate_name: str
    questions_evaluations: List[QuestionEvaluation]
    overall_score: float
    overall_percentage: float
    recommendation: str
    strengths: List[str]
    improvements: List[str]
```

## API Endpoints

### Interview Lifecycle
```
POST   /api/interviews
  → Creates new interview session
  ← Returns interview_id

GET    /api/interviews/{interview_id}/question
  → Gets next question
  ← Returns question or completed flag

POST   /api/interviews/{interview_id}/response
  → Submits answer
  ← Confirms submission

POST   /api/interviews/{interview_id}/complete
  → Finalizes interview
  ← Generates and returns report
```

### Report Retrieval
```
GET    /api/interviews/{interview_id}/report
  → Gets comprehensive report
  ← Returns detailed report with marks

GET    /api/reports?limit=10&skip=0
  → Lists all reports
  ← Returns paginated reports list

GET    /api/interviews/{interview_id}/evaluation
  → Gets simple evaluation (backward compat)
  ← Returns simplified eval
```

## Database Schema

### ai_interviews.reports Collection

```javascript
{
  "_id": ObjectId,
  "interview_id": String,
  "candidate_name": String,
  "candidate_email": String,
  "role": String,
  "experience_level": String,
  "skills": [String],
  "total_questions": Number,
  "answered_questions": Number,
  
  "questions_evaluations": [
    {
      "question_id": String,
      "question": String,
      "answer": String,
      "marks": Number(0-10),
      "max_marks": 10,
      "percentage": Number(0-100),
      "feedback": String,
      "correctness": String(excellent|good|fair|poor)
    }
  ],
  
  "overall_score": Number(0-100),
  "overall_percentage": Number(0-100),
  "total_marks": Number,
  "max_total_marks": Number,
  "recommendation": String(Strong Hire|Hire|Maybe|No Hire),
  "strengths": [String],
  "improvements": [String],
  "generated_at": Date,
  "interview_duration_seconds": Number
}
```

### Indexes
```javascript
db.reports.createIndex({ "interview_id": 1 })
db.reports.createIndex({ "generated_at": -1 })
db.reports.createIndex({ "candidate_email": 1 })
```

## Extending the System

### 1. Adding LLM Integration

**File to modify**: `backend/main.py`

```python
import openai

class LLMEvaluationService:
    @staticmethod
    async def evaluate_answer_with_llm(
        question: str,
        answer: str,
        role: str,
        skills: List[str]
    ):
        prompt = f"""
        Evaluate this {role} candidate's answer:
        
        Question: {question}
        Answer: {answer}
        Expected Skills: {', '.join(skills)}
        
        Provide:
        1. Marks (0-10)
        2. Feedback
        3. Correctness level
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response and return structured data
```

### 2. Custom Evaluation Rubric

**Add to models**:
```python
class EvaluationRubric(BaseModel):
    criteria: List[str]
    weights: List[float]  # Sum to 1.0
    
class RubricService:
    async def evaluate_with_rubric(
        self,
        answer: str,
        rubric: EvaluationRubric
    ):
        # Evaluate against custom rubric
        pass
```

### 3. Real-time Feedback

**Frontend enhancement**:
```typescript
// In app/interview/page.tsx
useEffect(() => {
  // After each response, evaluate and show feedback
  const evaluation = await getDetailedReport(interviewId)
  const lastEval = evaluation.questions_evaluations[-1]
  showFeedbackToast(lastEval.feedback)
}, [responses])
```

### 4. Analytics Dashboard

**New pages**:
- `app/analytics/page.tsx` - Overall statistics
- `app/reports/page.tsx` - Detailed reports list
- `app/candidates/page.tsx` - Candidate profiles

**API endpoints**:
```
GET /api/analytics/summary
GET /api/analytics/trends
GET /api/candidates/{email}
```

## Testing

### Unit Tests

```python
# test_evaluation_service.py
def test_answer_evaluation():
    service = AIEvaluationService()
    result = service.evaluate_answer(
        question="Explain REST APIs",
        answer="REST APIs use HTTP methods...",
        role="Backend Developer",
        skills=["APIs", "Python"]
    )
    assert result["marks"] >= 4
    assert result["marks"] <= 10
```

### Integration Tests

```python
# test_report_generation.py
async def test_report_generation():
    # Create interview
    # Submit responses
    # Complete interview
    # Verify report structure
    # Check database storage
```

### API Tests

```bash
# Test report endpoint
curl http://localhost:8000/api/interviews/{id}/report

# Test list endpoint
curl http://localhost:8000/api/reports?limit=10
```

## Performance Optimization

### Current Optimizations
- ✅ Database indexes on interview_id and generated_at
- ✅ Async/await for non-blocking operations
- ✅ Response caching in MongoDB
- ✅ Pagination for list endpoints

### Future Optimizations
- [ ] Redis caching layer
- [ ] Query result caching
- [ ] Background job queue for evaluations
- [ ] Batch report generation
- [ ] CDN for static assets

## Security Considerations

### Current Security
- ✅ Input validation (Pydantic)
- ✅ No SQL injection (MongoDB)
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ✅ Error handling (no stack traces exposed)

### Future Security
- [ ] API key authentication
- [ ] JWT tokens
- [ ] Rate limiting
- [ ] Encryption at rest
- [ ] Audit logging

## Deployment

### Local Development
```bash
python -m uvicorn backend.main:app --reload
```

### Production Deployment
```bash
# Using Gunicorn + Uvicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app

# Using Docker
docker-compose up -d
```

### Environment Variables
```env
MONGODB_URL=mongodb://user:pass@host:27017/
DATABASE_NAME=ai_interview_assistant
LOG_LEVEL=INFO
API_PORT=8000
```

## Monitoring & Logging

### Log Levels
```python
logger.debug("Detailed diagnostic information")
logger.info("General informational messages")
logger.warning("Warning messages")
logger.error("Error messages")
```

### Key Metrics to Monitor
- Average evaluation time
- Report generation latency
- Database query times
- API response times
- Error rates

## Troubleshooting Guide

### Common Issues

**Report not generating:**
1. Check MongoDB connection
2. Verify ai_interviews database exists
3. Check backend logs for errors
4. Run setup_mongodb.py again

**Slow evaluations:**
1. Check database indexes
2. Monitor network latency
3. Review evaluation algorithm
4. Consider caching

**Database connection:**
1. Verify MONGODB_URL
2. Test with mongosh
3. Check network connectivity
4. Review credentials

## Git Workflow

### Branch Structure
```
main (production)
├── develop (staging)
├── feature/ai-evaluation
├── feature/llm-integration
└── fix/bug-reports
```

### Commit Convention
```
feat: Add LLM integration
fix: Correct marks calculation
docs: Update API documentation
test: Add evaluation tests
perf: Optimize database queries
```

## Resources

### Documentation Files
- `FEATURES.md` - Feature overview
- `MIGRATION.md` - Migration guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `QUICKSTART_v2.md` - Getting started

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Next.js Documentation](https://nextjs.org/docs/)

---

**Last Updated**: December 18, 2025  
**Version**: 2.0  
**Maintainer**: Development Team
