# AI Interview Assistant - Quick Start Guide

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB 5.0+
- pnpm or npm

### 1. Clone & Install

```bash
# Frontend dependencies
pnpm install

# Backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. MongoDB Setup

```bash
# Start MongoDB (if not running)
mongosh

# Initialize databases
python scripts/setup_mongodb.py
```

### 3. Environment Configuration

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK_DATA=false
MONGODB_URL=mongodb://localhost:27017
```

### 4. Run Services

Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
pnpm dev
```

Visit: http://localhost:3000

## 📊 Key Features

### Answer Evaluation
Each answer is evaluated on:
- ✅ Technical accuracy (keyword matching)
- ✅ Clarity (structure and organization)
- ✅ Completeness (length and examples)
- ✅ Role relevance (specific terminology)

**Scoring**: 0-10 marks per answer → Converted to percentage

### Report Generation
Comprehensive reports include:
- Question-by-question evaluation
- Individual marks and feedback
- Overall score and recommendation
- Strengths and improvement areas

## 🔄 Interview Flow

```
Setup Interview
    ↓
Get Next Question
    ↓
User Submits Answer
    ↓
AI Evaluates Answer
    ↓
Provide Feedback
    ↓
Continue or Complete
    ↓
Generate Comprehensive Report
    ↓
View Results
```

## 📝 API Endpoints

### Interview Management
```
POST   /api/interviews                    Create interview
GET    /api/interviews                    List interviews
GET    /api/interviews/{id}               Get interview details
GET    /api/interviews/{id}/question      Get next question
POST   /api/interviews/{id}/response      Submit answer
POST   /api/interviews/{id}/complete      Complete interview
```

### Evaluation & Reports
```
GET    /api/interviews/{id}/evaluation    Get evaluation (simple)
GET    /api/interviews/{id}/report        Get detailed report
GET    /api/reports                       List all reports
```

## 🎯 Evaluation Scores

### Answer Marks
- **8-10**: Excellent (comprehensive, technical, well-structured)
- **6-7**: Good (solid answer with good detail)
- **4-5**: Fair (adequate but lacking depth)
- **<4**: Poor (insufficient or unclear)

### Overall Recommendation
- **≥85%**: Strong Hire 🟢
- **70-84%**: Hire 🔵
- **55-69%**: Maybe 🟡
- **<55%**: No Hire 🔴

## 🗄️ Database Structure

### ai_interview_assistant
Stores interviews, questions, and responses

### ai_interviews
Stores comprehensive reports with question-level evaluation

## 🧪 Testing

### Create Test Interview
```bash
curl -X POST http://localhost:8000/api/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "role": "Backend Developer",
    "experience_level": "mid",
    "skills": ["Python", "APIs", "Databases"],
    "duration": 30
  }'
```

### Get Report
```bash
curl http://localhost:8000/api/interviews/{interview_id}/report
```

## 📚 Documentation

- **FEATURES.md** - Detailed feature documentation
- **MIGRATION.md** - Migration guide from v1.0
- **IMPLEMENTATION_SUMMARY.md** - Complete implementation details
- **API.md** - API documentation (existing)
- **DEPLOYMENT.md** - Production deployment guide

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### MongoDB Connection Error
```bash
# Verify MongoDB is running
mongosh admin

# Check connection string
echo $MONGODB_URL
```

### Report Not Generating
1. Ensure all answers are submitted
2. Run `python scripts/setup_mongodb.py`
3. Check MongoDB collections exist

## ⚡ Performance Tips

1. **Indexes**: Already created automatically
2. **Async**: All operations are non-blocking
3. **Caching**: Reports cached in MongoDB
4. **Pagination**: Use limit/skip for large datasets

## 🚀 Deployment

### Production Checklist
- [ ] Set `NEXT_PUBLIC_USE_MOCK_DATA=false`
- [ ] Configure real MongoDB connection
- [ ] Set up SSL/TLS
- [ ] Configure CORS origins
- [ ] Set up monitoring
- [ ] Create database backups
- [ ] Review error logs

For full deployment guide: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📞 Support

### Common Issues

**Q: Why is my report taking long to generate?**
A: First report may take longer due to AI evaluation. Subsequent reports are faster.

**Q: Can I use mock data?**
A: Yes, set `NEXT_PUBLIC_USE_MOCK_DATA=true` for testing without backend.

**Q: How are answers evaluated?**
A: Using advanced NLP heuristics with keyword matching and structure analysis.

**Q: Can I export reports?**
A: Yes, reports are stored in MongoDB and can be exported via query.

## 🎓 Example Interview Scenario

```
Candidate: Alice (Backend Developer)
Role: Backend Developer
Duration: 30 minutes
Questions: 8

Results:
Q1: "Design an API" → 9/10 (Excellent)
Q2: "Database scaling" → 7/10 (Good)
Q3: "Error handling" → 6/10 (Good)
Q4: "Security" → 8/10 (Excellent)
...

Overall: 76.5% → Recommendation: HIRE ✅
Strengths: Strong technical knowledge, clear communication
Improvements: Include more real-world examples
```

## 🎉 You're Ready!

The AI Interview Assistant is now set up and ready to conduct intelligent technical interviews with comprehensive AI-powered evaluation.

Start by visiting: **http://localhost:3000**

---

**Need help?** Check the detailed documentation files or review the API documentation.

**Questions?** Review FEATURES.md for in-depth information about each capability.

**Happy interviewing!** 🚀
