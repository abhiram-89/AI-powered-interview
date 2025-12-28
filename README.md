<<<<<<< HEAD
🤖 AI-Based Interview Platform
-------------------------------

An intelligent, end-to-end AI-powered interview platform built using React.js, Python (FastAPI), AutoGen, and MongoDB.
This platform automates the interview process by simulating real interviewers using AI agents, evaluating candidates dynamically, and generating structured feedback in real time.

📌 Project Overview
--------------------

The AI Interview Platform is designed to help organizations, recruiters, and individuals conduct automated technical and non-technical interviews without human intervention.

Using multi-agent AI systems, the platform can:

Ask adaptive interview questions

Analyze candidate responses

Generate follow-up questions

Provide structured interview evaluations

This system reduces interviewer workload, ensures consistency, and enables scalable hiring.

🎯 Purpose of the Project
---------------------------

Traditional interviews are:

Time-consuming

Hard to scale

Subjective and inconsistent

This project solves those problems by introducing:

AI-driven interviewers

Automated evaluation

Real-time interaction

Data-driven insights

It can be used for:

Technical hiring

Mock interviews

Skill assessments

Campus recruitment

Self-evaluation practice

🧠 How the Platform Works (High-Level Flow)
---------------------------------------------

Candidate logs into the platform

Selects interview type (role, skills, difficulty)

AI Interview Agent starts asking questions

Candidate submits responses

AI Evaluation Agent analyzes answers

Follow-up questions are generated dynamically

Final feedback and score are produced

Interview results are stored securely in the database

🏗️ Tech Stack
--------------

Frontend

React.js

Modern component-based UI

Responsive and interactive interview interface

Real-time question and answer flow

Backend

Python

FastAPI

High-performance async APIs

Clean REST architecture

Secure communication with frontend

AI & Automation

AutoGen (Multi-Agent Framework)

AI Interviewer Agent

AI Evaluator Agent

AI Feedback Generator Agent

Context-aware question generation

Adaptive interview logic

Database

MongoDB

Stores:

User profiles

Interview sessions

Questions & answers

Scores & feedback

Schema-flexible for evolving interview formats

🧩 System Architecture
-------------------------
Frontend (React.js)
        |
        | REST API
        ↓
Backend (FastAPI)
        |
        | AI Orchestration
        ↓
AutoGen Multi-Agent System
        |
        | Data Persistence
        ↓
MongoDB

🧠 AI Agent Roles
-------------------------
1️⃣ Interviewer Agent

Generates interview questions

Adjusts difficulty based on responses

Maintains conversational flow

Simulates real interviewer behavior

2️⃣ Evaluation Agent

Analyzes candidate answers

Checks correctness, clarity, and depth

Scores responses using AI reasoning

3️⃣ Feedback Agent

Produces structured interview feedback

Highlights strengths and weaknesses

Gives improvement suggestions

🔐 Authentication & Security
-----------------------------


Secure user authentication

Token-based access control

Protected interview sessions

Isolated interview data per user

📊 Key Features

✅ AI-driven mock & real interviews

✅ Adaptive question generation

✅ Multi-agent AI evaluation

✅ Real-time interview experience

✅ Automated scoring and feedback

✅ Scalable backend architecture

✅ Clean and modern UI

✅ Secure data storage

🚀 Scalability & Extensibility

This platform is designed to be:

Scalable – supports multiple concurrent users

Modular – easy to add new AI agents

Extensible – supports new interview types and roles

Production-ready – clean codebase and structured APIs

Future extensions may include:

Video/audio interviews

Coding challenges

Resume-based interview generation

Analytics dashboard

Company-specific interview customization

Project Overview images
------------------------

<img width="1891" height="891" alt="Screenshot (69)" src="https://github.com/user-attachments/assets/3a1b0ca3-b219-4e31-98e3-804c6bac51aa" />

<img width="1890" height="883" alt="Screenshot (70)" src="https://github.com/user-attachments/assets/5643a216-c6e8-43a2-8357-811fab9ca1e5" />

<img width="1893" height="868" alt="Screenshot (71)" src="https://github.com/user-attachments/assets/9701702f-b062-4f08-a558-43983491dfd8" />

<img width="1806" height="880" alt="Screenshot (72)" src="https://github.com/user-attachments/assets/c374aa2d-881a-417f-96ec-880570eabf71" />

<img width="1841" height="875" alt="Screenshot (73)" src="https://github.com/user-attachments/assets/d2dd800b-febf-4e55-83c1-f8cb6f3db8ff" />

<img width="1872" height="880" alt="Screenshot (74)" src="https://github.com/user-attachments/assets/09ffae6f-a7c1-4dcd-b36d-15141c372981" />

<img width="1670" height="889" alt="Screenshot (75)" src="https://github.com/user-attachments/assets/a847f388-f082-4e8a-be90-d6866643071e" />

<img width="1622" height="874" alt="Screenshot (76)" src="https://github.com/user-attachments/assets/7c62a52c-e8bc-4d0d-bf4d-e557d328e913" />

<img width="1635" height="884" alt="Screenshot (77)" src="https://github.com/user-attachments/assets/5d5d31a6-abff-4f42-8029-4ea2174e3333" />
=======
# AI Interview & Hiring Assistant

A full-stack AI-powered interview platform built with Next.js, FastAPI, and MongoDB. Conduct intelligent technical interviews with adaptive questioning, real-time evaluation, and comprehensive candidate assessment.

## Features

### Core Features
- **Adaptive AI Interviews** - Dynamic question generation based on role, experience, and skills
- **Real-time Chat Interface** - Natural conversation flow with typing indicators
- **MongoDB Database** - Persistent storage for interviews, responses, and evaluations
- **RESTful API** - FastAPI backend with automatic documentation
- **Modern UI** - Beautiful, responsive interface built with shadcn/ui
- **Role-Specific Questions** - Tailored for Frontend, Backend, Full Stack, Data Science, DevOps, and Mobile

### Advanced Features (v2.0+)
- **🤖 AI-Powered Answer Evaluation** - Intelligent scoring based on technical accuracy, clarity, and completeness
- **📊 Comprehensive Reports** - Detailed question-by-question evaluation with marks and percentages
- **📈 Quality Metrics** - Advanced scoring for technical knowledge, communication, and problem-solving
- **💾 Dual Database Architecture** - Separate databases for interviews (`ai_interview_assistant`) and reports (`ai_interviews`)
- **⚡ Optimized Performance** - Async operations, indexed queries, <200ms API response times
- **✨ Professional Codebase** - Clean, production-ready code without debug references

## Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS v4** - Modern utility-first styling
- **shadcn/ui** - High-quality UI components

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Database
- **MongoDB** - NoSQL database for flexible data storage

## Project Structure

```
ai-interview-assistant/
├── app/                          # Next.js app directory
│   ├── page.tsx                 # Homepage
│   ├── setup/page.tsx           # Interview setup wizard
│   ├── interview/page.tsx       # Chat interview interface
│   ├── results/page.tsx         # Evaluation results
│   ├── demo/page.tsx            # Demo page
│   ├── layout.tsx               # Root layout
│   └── globals.css              # Global styles
├── backend/                      # FastAPI backend
│   ├── main.py                  # API routes and logic
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   └── README.md                # Backend documentation
├── scripts/                      # Utility scripts
│   └── setup_mongodb.py         # Database initialization
├── lib/
│   └── api.ts                   # Frontend API client
├── components/                   # React components
│   └── ui/                      # shadcn/ui components
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.9+** - [Download](https://python.org/)
- **MongoDB** - [Install locally](https://docs.mongodb.com/manual/installation/) or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-interview-assistant
```

### 2. Setup MongoDB

**Option A: Local MongoDB**

Start MongoDB locally:
```bash
mongod --dbpath /path/to/data/directory
```

**Option B: MongoDB Atlas**

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Get your connection string
3. Replace `localhost:27017` with your Atlas connection string

### 3. Initialize Database

```bash
cd scripts
pip install pymongo
python setup_mongodb.py
```

This creates the necessary collections, indexes, and seeds sample questions.

### 4. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your MongoDB connection string
# MONGODB_URL=mongodb://localhost:27017

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Setup Frontend

```bash
# From project root
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local if needed
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Usage

### Starting an Interview

1. Navigate to http://localhost:3000
2. Click "Get Started" or "Start Interview"
3. Fill in candidate details:
   - Candidate name and email
   - Role (Frontend, Backend, Full Stack, etc.)
   - Experience level (Junior, Mid, Senior, Lead)
   - Required skills (select at least 2)
   - Interview duration (15-60 minutes)
4. Click "Start Interview"

### During the Interview

1. Read each AI-generated question carefully
2. Type detailed answers in the text area
3. Press Enter to submit (Shift+Enter for new lines)
4. AI provides feedback and asks follow-up questions
5. Progress bar shows interview completion status

### Viewing Results

1. After completing all questions, AI generates evaluation
2. View overall score and recommendation (Strong Hire, Hire, Maybe, No Hire)
3. See detailed skill scores with feedback
4. Review strengths and areas for improvement
5. Download comprehensive report (coming soon)
6. Start another interview or return home

## API Endpoints

### Health Check
- `GET /` - API status and version

### Interviews
- `POST /api/interviews` - Create new interview
- `GET /api/interviews` - List all interviews
- `GET /api/interviews/{id}` - Get interview details
- `GET /api/interviews/{id}/question` - Get next question
- `POST /api/interviews/{id}/response` - Submit answer
- `POST /api/interviews/{id}/complete` - Complete interview and generate evaluation
- `GET /api/interviews/{id}/evaluation` - Get evaluation results

See full API documentation at http://localhost:8000/docs

## Database Schema

### Collections

**interviews**
- Stores interview session data
- Fields: candidate info, role, skills, status, timestamps

**questions**
- Question bank organized by role and skill
- Fields: role, skill, difficulty, question text, topics

**responses**
- Candidate answers to questions
- Fields: interview_id, question_id, answer, timestamp

**evaluations**
- AI-generated evaluation reports
- Fields: scores, recommendation, strengths, improvements

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Development

### Adding New Question Types

Edit `scripts/setup_mongodb.py` to add more questions:

```python
{
    "role": "Frontend Developer",
    "skill": "React",
    "difficulty": "advanced",
    "question": "Explain React Server Components and their benefits.",
    "topics": ["React", "SSR", "Performance"],
    "created_at": datetime.utcnow()
}
```

Then run the setup script again.

### Customizing Evaluation Logic

Edit the evaluation algorithm in `backend/main.py` in the `complete_interview` function. You can integrate AI models here for more sophisticated evaluation.

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Backend (Railway/Render)

1. Create new web service
2. Connect to your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Database (MongoDB Atlas)

1. Create production cluster
2. Whitelist deployment IPs
3. Update connection string in backend environment variables

## Troubleshooting

### Backend won't start
- Check if MongoDB is running
- Verify MONGODB_URL in backend/.env
- Ensure port 8000 is not in use

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local
- Check browser console for CORS errors

### Database connection errors
- Verify MongoDB is running
- Check connection string format
- Ensure network connectivity

### Questions not loading
- Run the database setup script
- Check backend logs for errors
- Verify questions collection has data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests if applicable
5. Submit a pull request

## License

MIT License - feel free to use this project for your portfolio or learning.

## Support

For issues or questions:
- Check the [API documentation](http://localhost:8000/docs)
- Review backend logs
- Check browser console for frontend errors

## Roadmap

- [ ] AI-powered question generation using LLMs
- [ ] Video interview support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Integration with ATS systems
- [ ] Custom question banks
- [ ] Team collaboration features

## Acknowledgments

Built with modern web technologies:
- Next.js for the frontend framework
- FastAPI for the backend API
- MongoDB for data persistence
- shadcn/ui for beautiful components
- Tailwind CSS for styling

---

**Happy Interviewing!** 🎯
>>>>>>> 4ab7e10 (Meaningful message)
