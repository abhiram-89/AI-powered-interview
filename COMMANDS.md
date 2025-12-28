# 🚀 COMMAND REFERENCE - AI Interview Assistant v2.0

## Quick Launch (Copy & Paste)

### Terminal 1 - Backend (Gemini AI Engine)
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant\backend
uvicorn main_v2:app --reload --port 8000
```

### Terminal 2 - Frontend (Web Interface)
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm dev
```

### Terminal 3 - MongoDB (Verify Connection)
```bash
mongosh
> use ai_interviews
> db.reports.find()
```

---

## URLs After Launch

| Component | URL |
|-----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MongoDB Shell | mongosh (localhost:27017) |

---

## One-Time Setup Commands

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Verify Gemini Installation
```bash
python -c "import google.generativeai; print('✓ Gemini installed')"
```

### 3. Verify MongoDB Connection
```bash
mongosh --eval "db.adminCommand('ping')"
```

### 4. Install Frontend Dependencies (if needed)
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm install
```

---

## Database Commands

### Check if ai_interviews Database Exists
```bash
mongosh
> show databases
> use ai_interviews
> show collections
```

### View Interview Reports
```bash
mongosh
> use ai_interviews
> db.reports.find().pretty()
```

### Count Reports
```bash
mongosh
> use ai_interviews
> db.reports.count()
```

### Get Latest Report
```bash
mongosh
> use ai_interviews
> db.reports.findOne({}, { sort: { generated_at: -1 } })
```

### Clear Reports (for Testing)
```bash
mongosh
> use ai_interviews
> db.reports.deleteMany({})
```

---

## Frontend Commands

### Install Dependencies
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm install
```

### Start Development Server
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm dev
```

### Build for Production
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm build
```

### Clean Build (if issues)
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
rm -r .next node_modules
pnpm install
pnpm dev
```

---

## Backend Commands

### Start Backend with v2.0 (Gemini AI)
```bash
cd backend
uvicorn main_v2:app --reload --port 8000
```

### Start Backend with v1.0 (Fallback, no AI)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Check Backend Logs (Already Running)
```bash
# View in the terminal where uvicorn is running
# Look for: ✓ Gemini AI model initialized
```

### Test API Endpoint
```bash
curl http://localhost:8000/docs
```

---

## Environment Configuration

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK_DATA=false
```

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_interviews
GEMINI_API_KEY=AIzaSyAgiTBFGwEgVNcnrP4oZwwKSpSTuigCrvc
PORT=8000
```

---

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Node/pnpm Version
```bash
pnpm --version
node --version
```

### Check MongoDB Running
```bash
mongosh --version
mongosh
```

### View Backend Startup Logs
```
Check terminal where uvicorn is running
Look for lines starting with ✓ or ✗
```

### Test Gemini Configuration
```bash
python -c "import os; print('API Key:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

### Clear Frontend Cache
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
rm -r .next
pnpm dev
```

---

## File Locations

| File | Path |
|------|------|
| Backend (v2.0) | `backend/main_v2.py` |
| Backend (v1.0) | `backend/main.py` |
| Frontend Interview | `app/interview/page.tsx` |
| Frontend Results | `app/results/page.tsx` |
| API Client | `lib/api.ts` |
| Backend Config | `backend/.env` |
| Frontend Config | `.env.local` |
| Requirements | `backend/requirements.txt` |

---

## Test Interview Flow Commands

### Step 1: Create Interview
```
Visit: http://localhost:3000
Enter: Name, Email, Role, Experience, Skills
Click: Start Interview
```

### Step 2: Monitor Backend
```
Watch terminal 1 (backend) for:
✓ Generated question for [role]
✓ Analyzed response - Marks: 8
```

### Step 3: Monitor Database
```bash
# In new terminal, keep watching:
mongosh
> use ai_interviews
> db.reports.find().pretty()
# Should see new report after interview completes
```

### Step 4: Verify Results
```
Visit: http://localhost:3000/results?id=[interview_id]
Check: Overall score, recommendation, details
```

---

## Performance Tuning

### Increase Backend Timeout (if slow)
```
Edit backend/main_v2.py:
Add: timeout = 60  # seconds
```

### Optimize Frontend Rendering
```
Edit app/interview/page.tsx:
Look for: fetchNextQuestion()
Adjust timing if needed
```

### Database Query Optimization
```bash
mongosh
> use ai_interviews
> db.reports.find().explain("executionStats")
```

---

## Deployment Preparation

### Before Production:
1. Set `NEXT_PUBLIC_USE_MOCK_DATA=false` in `.env.local`
2. Set `GEMINI_API_KEY` in backend `/.env`
3. Change `allow_origins=["*"]` to specific domain in `main_v2.py`
4. Enable HTTPS on frontend
5. Move secrets to environment variables

### Deploy Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main_v2:app --host 0.0.0.0 --port 8000
```

### Deploy Frontend:
```bash
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant
pnpm build
pnpm start
```

---

## Useful One-Liners

### Check Everything Running
```bash
# Backend running?
curl -s http://localhost:8000 | jq .status

# Frontend running?
curl -s http://localhost:3000 | grep -q "DOCTYPE" && echo "Frontend OK"

# MongoDB running?
mongosh --eval "db.adminCommand('ping')"
```

### Quick Status Check
```bash
echo "=== Backend ===" && curl -s http://localhost:8000/docs | head -1
echo "=== Frontend ===" && curl -s http://localhost:3000 | head -1
echo "=== MongoDB ===" && mongosh --eval "db.adminCommand('ping')" 2>/dev/null
```

### Reset Everything
```bash
# Stop all services (Ctrl+C in each terminal)
cd backend && rm -r __pycache__ .pytest_cache
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant && rm -r .next
mongosh << EOF
use ai_interviews
db.reports.deleteMany({})
EOF
# Restart all services
```

---

## Common Issues Quick Fixes

| Issue | Command |
|-------|---------|
| Backend won't start | `cd backend && uvicorn main_v2:app --reload` |
| Frontend won't load | `cd c:\Users\ABHIRAM\Documents\ai-interview-assistant && pnpm install` |
| MongoDB connection fails | `mongosh` (to test connection) |
| Gemini not responding | Check: `echo $env:GEMINI_API_KEY` |
| Port 8000 in use | `netstat -an \| findstr :8000` |
| Port 3000 in use | `netstat -an \| findstr :3000` |

---

## Documentation Files

Read in this order:
1. **START_HERE_AI_v2.md** ← START HERE!
2. **QUICKSTART_AI_v2.md**
3. **IMPLEMENTATION_COMPLETE.md**
4. **This file** (command reference)

---

## Support

- **API Issues**: Check http://localhost:8000/docs
- **Database Issues**: Use `mongosh` directly
- **Frontend Issues**: Check browser console (F12)
- **Backend Logs**: Check terminal where uvicorn runs
- **Gemini Issues**: Verify API key in `backend/.env`

---

**Ready to launch? Start with:**
```bash
# Terminal 1
cd backend && uvicorn main_v2:app --reload

# Terminal 2
cd c:\Users\ABHIRAM\Documents\ai-interview-assistant && pnpm dev

# Then visit: http://localhost:3000
```

✨ **Good luck!** ✨
