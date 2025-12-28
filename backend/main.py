"""
Agentic AI Interview Platform Backend
- Dynamic question generation based on selected skills
- AI-powered answer verification  
- Dynamic report generation
- Everything powered by Gemini AI (agentic process)
- Uses MongoDB for data persistence
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import uuid
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import google.generativeai as genai
import re
from typing import Tuple

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "ai_interviews"
COLLECTION_INTERVIEWS = "interviews"
COLLECTION_QUESTIONS = "questions"
COLLECTION_EVALUATIONS = "evaluations"

# Validate API key
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not found. Using development mode.")
    GEMINI_API_KEY = "development_mode"
    DEVELOPMENT_MODE = True
else:
    DEVELOPMENT_MODE = False

# Initialize Gemini AI
if not DEVELOPMENT_MODE:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI
app = FastAPI(title="Agentic Interview AI Platform")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MongoDB Connection
# ============================================================

def get_mongodb_client():
    """Get MongoDB client with connection pooling"""
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except ServerSelectionTimeoutError:
        print("⚠️  MongoDB connection failed. Using development mode.")
        return None

def get_database():
    """Get database instance"""
    client = get_mongodb_client()
    if client is None:
        return None
    return client[DB_NAME]


# In-memory store used when MongoDB is not available (development mode)
DEV_STORE: Dict[str, Dict[str, Any]] = {
    "interviews": {},  # interview_id -> interview_doc
    "questions": {}    # interview_id -> list of question docs
}


# ================= Helper: Robust model response parsing =================
def extract_json_from_text(text: str) -> Optional[str]:
    """Attempt to extract a JSON object or array from arbitrary model text.

    Returns the JSON substring if found, else None.
    """
    if not text:
        return None

    # Find first JSON object/array start
    for start_char in ('{', '['):
        start_idx = text.find(start_char)
        if start_idx == -1:
            continue

        stack = []
        for i in range(start_idx, len(text)):
            ch = text[i]
            if ch in '{[':
                stack.append(ch)
            elif ch in '}]':
                if not stack:
                    break
                open_ch = stack.pop()
                if (open_ch == '{' and ch != '}') or (open_ch == '[' and ch != ']'):
                    break
                if not stack:
                    candidate = text[start_idx:i+1]
                    return candidate

    # Fallback: regex to grab first {...}
    m = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.DOTALL)
    if m:
        return m.group(0)

    return None


def safe_parse_json_from_model(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON substring and parse it into Python object. Returns None on failure."""
    try:
        json_sub = extract_json_from_text(text)
        if not json_sub:
            return None
        return json.loads(json_sub)
    except Exception:
        return None


def call_model_safe(model, prompt: str) -> str:
    """Call the generative model safely and return raw text output."""
    try:
        response = model.generate_content(prompt)
        # response may expose .text or be a string-like object
        resp_text = getattr(response, 'text', None)
        if resp_text is None:
            resp_text = str(response)
        return resp_text
    except Exception as e:
        # Re-raise so callers can fallback
        raise

# ============================================================
# Pydantic Models
# ============================================================

class SkillSelection(BaseModel):
    """Skills selected for interview"""
    skill_name: str
    proficiency_level: str  # "beginner", "intermediate", "advanced"
    experience_years: Optional[int] = None

class InterviewSetupRequest(BaseModel):
    """Initial interview setup"""
    candidate_name: str
    role: str  # "frontend", "backend", "fullstack", etc.
    experience: str  # "junior", "mid", "senior"
    selected_skills: List[SkillSelection]
    interview_duration_minutes: int = 30

class InterviewRecord(BaseModel):
    """Single Q&A record"""
    question_id: str
    question_number: int
    question_text: str
    question_context: str  # Why this question was asked
    answer: str
    timestamp: datetime
    answer_quality_notes: Optional[str] = None

class SubmitAnswerRequest(BaseModel):
    """Submit answer to current question"""
    question_id: str
    answer: str
    time_taken_seconds: int

class CompleteInterviewRequest(BaseModel):
    """Complete interview with all answers"""
    interview_history: List[InterviewRecord]

class NextQuestionResponse(BaseModel):
    """Response with next question"""
    question_id: str
    question_number: int
    total_questions: int
    question_text: str
    skill_being_tested: str
    difficulty_level: str
    completed: bool

# ============================================================
# Development Mode Mock Data
# ============================================================

def get_mock_questions(role: str, skills: List[Dict], total: int = 8):
    """Generate DIVERSE mock questions for development mode - FIXED"""
    import random
    
    if not skills:
        skills = [{"skill_name": "General", "proficiency_level": "intermediate"}]
    
    # DIVERSE question templates across different categories
    question_templates = {
        "project_experience": [
            "Describe a challenging project where you used {skill}. What technical decisions did you make and why?",
            "Walk me through how you architected a solution using {skill}. What were the key design considerations?",
            "Tell me about a time when you had to optimize performance in a {skill} application. What was your approach?",
            "Explain a real-world problem you solved using {skill}. What alternatives did you consider?"
        ],
        "technical_deep_dive": [
            "How does {skill} handle state management? Explain with examples from your experience.",
            "What are the most common pitfalls when working with {skill}, and how do you avoid them?",
            "Compare {skill} with alternative approaches. When would you choose each?",
            "Explain the internals of how {skill} works. What happens under the hood?"
        ],
        "problem_solving": [
            "If you encountered a memory leak in {skill}, how would you debug and resolve it?",
            "Design a scalable system that uses {skill} for real-time data processing. What would be your approach?",
            "How would you scale a {skill} application to handle 10x traffic? Walk me through your strategy.",
            "Describe how you would implement authentication and authorization using {skill}. What challenges would you anticipate?"
        ],
        "best_practices": [
            "What are your go-to best practices when working with {skill}?",
            "How do you ensure code quality and maintainability in {skill} projects?",
            "Describe your testing strategy for {skill} applications.",
            "How do you stay updated with {skill}? What recent changes have impacted your work?"
        ],
        "collaboration": [
            "How do you explain {skill} concepts to non-technical stakeholders?",
            "Describe a code review where you gave or received feedback about {skill} implementation.",
            "How have you mentored others in {skill}? What approach do you take?",
            "Tell me about a time you had to make a technical compromise in a {skill} project. How did you communicate this?"
        ]
    }
    
    questions = []
    categories = list(question_templates.keys())
    
    for i in range(total):
        # Select skill for this question
        skill = skills[i % len(skills)]
        skill_name = skill.get('skill_name', 'General')
        
        # Select category and template
        category = categories[i % len(categories)]
        templates = question_templates[category]
        template = templates[i % len(templates)]
        
        # Generate unique question text
        question_text = template.replace("{skill}", skill_name)
        
        # Determine difficulty
        if i < total // 3:
            difficulty = "easy"
        elif i < 2 * total // 3:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        # Create unique question ID
        qid = f"q_{i+1}_{category[:4]}_{re.sub(r'[^a-zA-Z0-9]', '', skill_name)}"
        
        questions.append({
            "id": qid,
            "number": i + 1,
            "question": question_text,
            "skill_tested": skill_name,
            "difficulty": difficulty,
            "category": category,
            "expected_key_points": [
                f"Demonstrates practical understanding of {skill_name}",
                f"Provides specific examples or details",
                f"Shows decision-making and reasoning",
                f"Explains trade-offs and alternatives"
            ],
            "why_this_question": f"Evaluates {category.replace('_', ' ')} with {skill_name}",
            "follow_up_prompt": f"Can you elaborate on the technical details of your {skill_name} implementation?"
        })
    
    # Shuffle to create natural variety
    random.shuffle(questions)
    
    # Re-number after shuffle
    for idx, q in enumerate(questions, start=1):
        q["number"] = idx
    
    return questions

def get_mock_analysis(answer: str, expected_key_points: Optional[List[str]] = None):
    """Generate smarter mock analysis for development mode.

    - Scores based on word count, presence of expected key points, and basic readability.
    - Detects gibberish-like input and assigns a low score.
    """
    # Basic sanitization
    if not answer:
        return {
            "overall_score": 10,
            "key_points_covered": [],
            "missing_points": expected_key_points or [],
            "communication_quality": "poor",
            "technical_accuracy": "poor",
            "depth_of_knowledge": "superficial",
            "feedback_to_candidate": "No answer provided. Please respond with a clear, structured explanation."
        }

    words = answer.split()
    word_count = len(words)

    # Heuristic gibberish detection: very low distinct letter ratio or repeated random characters
    distinct_chars = len(set(re.sub(r"\s+", "", answer)))
    gibberish_score_penalty = 0
    if distinct_chars < 5 or re.search(r"[a-z]{0,2}[0-9]{3,}|^[-_]{3,}|^[qwertyuiopasdfghjklzxcvbnm]{6,}$", answer, re.IGNORECASE):
        gibberish_score_penalty = 40

    # Base score from length
    base = min(60, 10 + word_count * 2)

    # Check expected key points
    covered = []
    missing = []
    if expected_key_points:
        for kp in expected_key_points:
            # simple keyword presence check (case-insensitive)
            key = re.sub(r"[^a-zA-Z0-9 ]", "", kp).strip().lower()
            if key and key.split()[0] and re.search(re.escape(key.split()[0]), answer, re.IGNORECASE):
                covered.append(kp)
            else:
                missing.append(kp)

    # Additional boost for covering key points
    kp_bonus = min(30, len(covered) * 10)

    # Communication quality heuristic
    if word_count < 8:
        comm = "poor"
    elif word_count < 25:
        comm = "adequate"
    else:
        comm = "good"

    technical = "poor"
    depth = "superficial"
    if len(covered) >= max(1, (len(expected_key_points or []) // 2)):
        technical = "good"
        depth = "adequate" if word_count < 40 else "good"

    score = base + kp_bonus - gibberish_score_penalty
    score = max(5, min(100, int(score)))

    feedback = []
    if gibberish_score_penalty:
        feedback.append("Answer appears noisy or contains random characters; please provide a clearer response.")
    if covered:
        feedback.append("You covered: " + ", ".join([c for c in covered]))
    if missing:
        feedback.append("Missing: " + ", ".join([m for m in missing]))
    if not feedback:
        feedback_text = f"Good answer. Score: {score}/100"
    else:
        feedback_text = " ".join(feedback) + f" Score: {score}/100"

    return {
        "overall_score": score,
        "key_points_covered": covered or ["Provided relevant examples"],
        "missing_points": missing or ["Could add more technical depth"],
        "communication_quality": comm,
        "technical_accuracy": technical,
        "depth_of_knowledge": depth,
        "feedback_to_candidate": feedback_text
    }

def get_mock_report(candidate_name: str, role: str, answers_count: int, 
                    interview_data: Optional[List[Dict]] = None,
                    individual_scores: Optional[Dict[str, float]] = None):
    """Generate DYNAMIC mock report based on actual answer scores - COMPLETELY FIXED"""
    
    # PRIORITY 1: Calculate from actual interview_data (complete answer analysis)
    if interview_data:
        # Extract all answer scores
        all_scores = [qa.get('overall_score', 0) for qa in interview_data if qa.get('overall_score')]
        
        if all_scores:
            # Calculate REAL overall score as average of all answers
            overall = int(sum(all_scores) / len(all_scores))
            
            # Technical score from actual answers
            technical = int(sum(all_scores) / len(all_scores))
            
            # Communication derived from actual quality ratings
            communication_qualities = [qa.get('communication_quality', 'adequate') for qa in interview_data]
            comm_score_map = {"poor": 30, "adequate": 60, "good": 80, "excellent": 95}
            comm_scores = [comm_score_map.get(cq, 60) for cq in communication_qualities]
            communication = int(sum(comm_scores) / len(comm_scores)) if comm_scores else 60
            
            # Cultural fit from depth of knowledge
            depth_qualities = [qa.get('depth_of_knowledge', 'adequate') for qa in interview_data]
            depth_score_map = {"superficial": 40, "adequate": 65, "good": 80, "deep": 95}
            depth_scores = [depth_score_map.get(dq, 65) for dq in depth_qualities]
            cultural = int(sum(depth_scores) / len(depth_scores)) if depth_scores else 65
        else:
            # Fallback if no scores in interview_data
            overall = 50
            technical = 50
            communication = 50
            cultural = 50
    
    # PRIORITY 2: Use individual skill scores if interview_data not available
    elif individual_scores:
        scores = list(individual_scores.values())
        overall = int(sum(scores) / len(scores)) if scores else 50
        technical = int(sum(scores) / len(scores)) if scores else 50
        communication = max(40, int(overall * 0.9))
        cultural = max(40, int(overall * 0.85))
    
    # PRIORITY 3: Absolute fallback
    else:
        overall = 50
        technical = 50
        communication = 50
        cultural = 50

    # DYNAMIC recommendation based on ACTUAL score
    if overall >= 85:
        recommendation = "strong-hire"
        reasoning = f"{candidate_name} demonstrated excellent performance across all areas with an overall score of {overall}/100. Strong technical skills and communication."
        strengths = [
            f"Exceptional technical performance (scored {technical}/100)",
            f"Excellent communication skills (scored {communication}/100)",
            "Consistently high-quality answers with good depth"
        ]
    elif overall >= 70:
        recommendation = "hire"
        reasoning = f"{candidate_name} showed solid performance with an overall score of {overall}/100. Good technical foundation and clear communication."
        strengths = [
            f"Strong technical fundamentals (scored {technical}/100)",
            f"Good communication skills (scored {communication}/100)",
            "Practical experience evident in responses"
        ]
    elif overall >= 55:
        recommendation = "maybe"
        reasoning = f"{candidate_name} demonstrated moderate performance with an overall score of {overall}/100. Some areas need improvement but shows potential."
        strengths = [
            f"Adequate technical knowledge (scored {technical}/100)",
            "Shows willingness to learn",
            "Some practical experience evident"
        ]
    else:
        recommendation = "no-hire"
        reasoning = f"{candidate_name} scored {overall}/100 overall. Significant gaps in technical knowledge and communication need to be addressed."
        strengths = [
            "Shows basic understanding of some concepts",
            "Potential for growth with training"
        ]

    # DYNAMIC development areas based on actual scores
    development_areas = []
    if technical < 70:
        development_areas.append("Needs to deepen technical knowledge and provide more detailed explanations")
    if communication < 70:
        development_areas.append("Could improve clarity and structure in communication")
    if cultural < 70:
        development_areas.append("Should demonstrate deeper understanding of concepts with real-world examples")
    if not development_areas:
        development_areas = ["Continue building on strong foundation", "Stay updated with latest best practices"]

    return {
        "overall_score": overall,
        "technical_score": technical,
        "communication_score": communication,
        "cultural_fit_score": cultural,
        "recommendation": recommendation,
        "final_reasoning": reasoning,
        "strengths": strengths,
        "development_areas": development_areas,
        "role_fit_assessment": f"Based on {answers_count} responses with {overall}/100 overall score, candidate shows {'strong' if overall >= 70 else 'moderate' if overall >= 55 else 'developing'} fit for {role} position.",
        "three_month_plan": [
            "Focus on areas scoring below 70/100" if min(technical, communication, cultural) < 70 else "Continue building on strengths",
            "Practice explaining technical concepts with more depth" if communication < 75 else "Maintain excellent communication practices",
            "Build more complex real-world projects" if technical < 75 else "Tackle advanced architectural challenges"
        ],
        "next_round_questions": [
            "Can you walk through a complex system design challenge?" if technical >= 70 else "Let's dive deeper into fundamental concepts",
            "How do you approach mentoring junior developers?" if overall >= 75 else "Tell me more about your learning process"
        ]
    }

# ============================================================
# Agentic AI Question Generator
# ============================================================

class Agentic_QuestionGenerator:
    """
    Agentic system for generating questions dynamically
    Adapts question difficulty and topic based on skills and performance
    """
    
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        if not DEVELOPMENT_MODE:
            self.model = genai.GenerativeModel(model_name)
        self.conversation_history = []
    
    def generate_initial_questions(
        self,
        candidate_name: str,
        role: str,
        experience: str,
        selected_skills: List[Dict[str, str]],
        total_questions: int = 8,
        exclude_question_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Agentic process: Generate initial question set
        - Considers role and skills
        - Matches experience level
        - Creates contextual, flowing questions
        """
        
        if DEVELOPMENT_MODE:
            print("🔧 Development mode: Using mock questions")
            return get_mock_questions(role, selected_skills, total_questions)
        
        skills_str = ", ".join([
            f"{s['skill_name']} ({s['proficiency_level']})"
            for s in selected_skills
        ])
        exclude_text = ""
        if exclude_question_ids:
            exclude_text = "\nEXCLUDE THESE QUESTION IDS (do not repeat): " + ", ".join(exclude_question_ids) + "\n"
        
        prompt = f"""You are an expert technical interviewer for a {role.upper()} position.

CONTEXT:
- Candidate: {candidate_name}
- Experience Level: {experience}
- Skills to assess: {skills_str}
- Total questions: {total_questions}

TASK: Generate {total_questions} technical interview questions that:
1. Are specifically tailored to the candidate's selected skills
2. Match their experience level ({experience})
3. Create a natural flow (start easier, progressively harder)
4. Mix different question types (theory, practical, problem-solving, communication)
5. Are designed to reveal genuine competency

IMPORTANT:
- Each question should test specific skill areas
- Include reasoning for why each question assesses that skill
- Make questions conversational and not robotic
- Avoid generic questions - be specific to their skills
- Distribute questions across different skills

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "questions": [
    {{
      "id": "q_1",
      "number": 1,
      "question": "exact question text here",
      "skill_tested": "specific skill name",
      "difficulty": "easy/medium/hard",
      "expected_key_points": ["point1", "point2", "point3"],
      "why_this_question": "explanation of why this tests their skill",
      "follow_up_prompt": "optional follow-up if initial answer is weak"
    }}
  ]
}}"""
        
        try:
            response_text = call_model_safe(self.model, prompt)
            parsed = safe_parse_json_from_model(response_text)
            if parsed and isinstance(parsed, dict):
                return parsed.get("questions", [])
            # final fallback: try direct json.loads of raw text
            try:
                parsed_raw = json.loads(response_text)
                return parsed_raw.get("questions", [])
            except Exception:
                print("⚠️  Could not parse model JSON output; falling back to mock questions")
                return get_mock_questions(role, selected_skills, total_questions)
        except Exception as e:
            print(f"❌ Error generating questions: {e}")
            print("🔧 Falling back to mock questions")
            return get_mock_questions(role, selected_skills, total_questions)

# ============================================================
# Agentic AI Answer Analyzer
# ============================================================

class Agentic_AnswerAnalyzer:
    """
    Agentic system for analyzing candidate answers
    Evaluates: technical accuracy, depth, communication, completeness
    """
    
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        if not DEVELOPMENT_MODE:
            self.model = genai.GenerativeModel(model_name)
    
    def analyze_single_answer(
        self,
        question_text: str,
        answer_text: str,
        expected_key_points: List[str],
        skill_tested: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """
        Agentic analysis of a single answer
        Returns structured evaluation with scores and feedback
        """
        
        if DEVELOPMENT_MODE:
            print(f"🔧 Development mode: Using mock analysis")
            return get_mock_analysis(answer_text, expected_key_points)
        
        expected_points_str = "\n".join([f"- {p}" for p in expected_key_points])
        
        prompt = f"""You are an expert technical interviewer analyzing a candidate's answer.

QUESTION: {question_text}
SKILL TESTED: {skill_tested}
DIFFICULTY: {difficulty}

EXPECTED KEY POINTS:
{expected_points_str}

CANDIDATE'S ANSWER:
{answer_text}

TASK: Analyze the answer comprehensively and provide structured feedback.

Return ONLY valid JSON (no markdown):
{{
  "overall_score": 0-100,
  "key_points_covered": ["list of points they mentioned"],
  "missing_points": ["important points they missed"],
  "communication_quality": "poor/adequate/good/excellent",
  "technical_accuracy": "poor/adequate/good/excellent",
  "depth_of_knowledge": "superficial/adequate/good/deep",
  "feedback_to_candidate": "constructive 2-3 sentence feedback"
}}"""
        
        try:
            response_text = call_model_safe(self.model, prompt)
            parsed = safe_parse_json_from_model(response_text)
            if parsed and isinstance(parsed, dict):
                return parsed
            # try direct load
            try:
                return json.loads(response_text)
            except Exception:
                print("⚠️  Could not parse model JSON for analysis; falling back to mock analysis")
                return get_mock_analysis(answer_text, expected_key_points)
        except Exception as e:
            print(f"❌ Error analyzing answer: {e}")
            print("🔧 Falling back to mock analysis")
            return get_mock_analysis(answer_text, expected_key_points)

# ============================================================
# Agentic AI Report Generator
# ============================================================

class Agentic_ReportGenerator:
    """
    Agentic system for generating comprehensive interview reports
    Synthesizes all answers and makes hiring recommendations
    """
    
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        if not DEVELOPMENT_MODE:
            self.model = genai.GenerativeModel(model_name)
    
    def generate_comprehensive_report(
        self,
        candidate_name: str,
        role: str,
        experience: str,
        selected_skills: List[Dict],
        interview_data: List[Dict],
        individual_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Agentic process: Generate comprehensive evaluation report
        Synthesizes performance across all questions
        """
        
        if DEVELOPMENT_MODE:
            print(f"🔧 Development mode: Using DYNAMIC mock report with actual scores")
            return get_mock_report(candidate_name, role, len(interview_data), 
                                 interview_data=interview_data,
                                 individual_scores=individual_scores)
        
        # Prepare interview summary
        interview_summary = []
        for idx, qa in enumerate(interview_data, 1):
            interview_summary.append(
                f"Q{idx}: {qa.get('question_text', 'N/A')}\n"
                f"Answer: {qa.get('answer_text', 'N/A')[:200]}...\n"
                f"Score: {qa.get('overall_score', 0)}/100\n"
            )
        
        summary_text = "\n".join(interview_summary)
        skills_str = ", ".join([s.get('skill_name', '') for s in selected_skills])
        
        prompt = f"""You are a senior technical hiring manager reviewing an interview.

CANDIDATE: {candidate_name}
ROLE: {role}
EXPERIENCE: {experience}
SKILLS ASSESSED: {skills_str}

INTERVIEW SUMMARY:
{summary_text}

SKILL SCORES:
{json.dumps(individual_scores, indent=2)}

TASK: Generate a comprehensive hiring evaluation report.

Return ONLY valid JSON (no markdown):
{{
  "overall_score": 0-100,
  "technical_score": 0-100,
  "communication_score": 0-100,
  "cultural_fit_score": 0-100,
  "recommendation": "strong-hire/hire/maybe/no-hire",
  "final_reasoning": "2-3 sentence summary of recommendation",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "development_areas": ["area 1", "area 2"],
  "role_fit_assessment": "detailed paragraph on role fit",
  "three_month_plan": ["goal 1", "goal 2", "goal 3"],
  "next_round_questions": ["question 1", "question 2"]
}}"""
        
        try:
            response_text = call_model_safe(self.model, prompt)
            parsed = safe_parse_json_from_model(response_text)
            if parsed and isinstance(parsed, dict):
                return parsed
            try:
                return json.loads(response_text)
            except Exception:
                print("⚠️  Could not parse model JSON for report; falling back to dynamic mock report")
                return get_mock_report(candidate_name, role, len(interview_data),
                                     interview_data=interview_data,
                                     individual_scores=individual_scores)
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            print("🔧 Falling back to dynamic mock report")
            return get_mock_report(candidate_name, role, len(interview_data),
                                 interview_data=interview_data,
                                 individual_scores=individual_scores)

# Initialize AI components
question_generator = Agentic_QuestionGenerator()
answer_analyzer = Agentic_AnswerAnalyzer()
report_generator = Agentic_ReportGenerator()

# ============================================================
# API Endpoints
# ============================================================

@app.post("/api/interviews/create")
async def create_interview(request: InterviewSetupRequest):
    """
    Create new interview session
    Agentic: Generates personalized questions based on role and skills
    """
    try:
        db = get_database()
        
        # Generate unique interview ID
        interview_id = str(uuid.uuid4())
        
        # Convert Pydantic models to dicts
        skills_list = [skill.model_dump() for skill in request.selected_skills]
        
        # Generate questions using agentic AI
        print(f"🤖 Generating questions for {request.candidate_name}...")
        questions = question_generator.generate_initial_questions(
            candidate_name=request.candidate_name,
            role=request.role,
            experience=request.experience,
            selected_skills=skills_list,
            total_questions=8
        )
        
        # Create interview record
        interview_doc = {
            "interview_id": interview_id,
            "candidate_name": request.candidate_name,
            "role": request.role,
            "experience": request.experience,
            "selected_skills": skills_list,
            "total_questions": len(questions),
            "current_question": 0,
            "status": "in_progress",
            "created_at": datetime.utcnow(),
            "answers": [],
            # Track asked question ids so the generator can avoid repeats
            "asked_question_ids": [],
            # Store per-question structured evaluations (analysis objects)
            "evaluations": [],
            # Final aggregated report (populated after all questions answered)
            "final_report": None,
            "skill_scores": {}
        }
        
        # Store in database (if available) or in DEV_STORE when in development mode
        if db is not None:
            db[COLLECTION_INTERVIEWS].insert_one(interview_doc)

            # Remove any existing questions for this interview_id to avoid duplicates
            try:
                db[COLLECTION_QUESTIONS].delete_many({"interview_id": interview_id})
            except Exception:
                pass

            # Store questions
            for q in questions:
                question_doc = {
                    "interview_id": interview_id,
                    "question_id": q["id"],
                    "number": q["number"],
                    "text": q["question"],
                    "skill_tested": q["skill_tested"],
                    "difficulty": q["difficulty"],
                    "expected_key_points": q.get("expected_key_points", []),
                    "why_this_question": q.get("why_this_question", ""),
                    "follow_up_prompt": q.get("follow_up_prompt", "")
                }
                db[COLLECTION_QUESTIONS].insert_one(question_doc)
        else:
            # Development mode: persist into DEV_STORE so subsequent endpoints can use them
            DEV_STORE["interviews"][interview_id] = interview_doc
            stored_qs = []
            for q in questions:
                stored_qs.append({
                    "interview_id": interview_id,
                    "question_id": q["id"],
                    "number": q["number"],
                    "text": q["question"],
                    "skill_tested": q["skill_tested"],
                    "difficulty": q["difficulty"],
                    "expected_key_points": q.get("expected_key_points", []),
                    "why_this_question": q.get("why_this_question", ""),
                    "follow_up_prompt": q.get("follow_up_prompt", "")
                })
            DEV_STORE["questions"][interview_id] = stored_qs
        
        print(f"✅ Interview created: {interview_id}")
        
        return {
            "success": True,
            "interview_id": interview_id,
            "total_questions": len(questions),
            "message": f"Generated {len(questions)} personalized questions"
        }
    
    except Exception as e:
        print(f"❌ Error creating interview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/interviews/{interview_id}/next-question")
async def get_next_question(interview_id: str):
    """
    Get next question in the interview
    Returns question or completion status
    """
    try:
        db = get_database()
        
        if db is None:
            # Development mode: pull from in-memory DEV_STORE
            interview = DEV_STORE["interviews"].get(interview_id)
            questions = DEV_STORE["questions"].get(interview_id, [])
            if not interview or not questions:
                # no interview found in dev store
                return NextQuestionResponse(
                    question_id="",
                    question_number=0,
                    total_questions=0,
                    question_text="",
                    skill_being_tested="",
                    difficulty_level="",
                    completed=True
                )

            current_q_num = interview.get("current_question", 0)
            total_questions = interview.get("total_questions", len(questions))

            if current_q_num >= total_questions:
                return NextQuestionResponse(
                    question_id="",
                    question_number=current_q_num,
                    total_questions=total_questions,
                    question_text="",
                    skill_being_tested="",
                    difficulty_level="",
                    completed=True
                )

            # Skip any questions that were already marked as asked
            asked_ids = interview.get("asked_question_ids", []) or []
            q = None
            for idx in range(current_q_num, len(questions)):
                candidate = questions[idx]
                if candidate.get("question_id") not in asked_ids:
                    q = candidate
                    break

            if q is None:
                return NextQuestionResponse(
                    question_id="",
                    question_number=current_q_num,
                    total_questions=total_questions,
                    question_text="",
                    skill_being_tested="",
                    difficulty_level="",
                    completed=True
                )

            # Mark this question as asked in the dev store
            if q.get("question_id") not in interview.get("asked_question_ids", []):
                interview.setdefault("asked_question_ids", []).append(q.get("question_id"))

            return NextQuestionResponse(
                question_id=q["question_id"],
                question_number=q["number"],
                total_questions=total_questions,
                question_text=q["text"],
                skill_being_tested=q.get("skill_tested", ""),
                difficulty_level=q.get("difficulty", ""),
                completed=False
            )
        
        # Get interview
        interview = db[COLLECTION_INTERVIEWS].find_one(
            {"interview_id": interview_id}
        )
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        current_q_num = interview["current_question"]
        total_questions = interview["total_questions"]
        
        # Check if completed
        if current_q_num >= total_questions:
            return NextQuestionResponse(
                question_id="",
                question_number=current_q_num,
                total_questions=total_questions,
                question_text="",
                skill_being_tested="",
                difficulty_level="",
                completed=True
            )
        
        # Get next question, skipping IDs already asked
        asked_ids = interview.get("asked_question_ids", []) or []

        # Try to find next question number > current_q_num that isn't asked yet
        question = None
        for num in range(current_q_num + 1, total_questions + 1):
            q = db[COLLECTION_QUESTIONS].find_one({
                "interview_id": interview_id,
                "number": num
            })
            if not q:
                continue
            if q.get("question_id") in asked_ids:
                continue
            question = q
            break

        if not question:
            # No unasked questions remain
            return NextQuestionResponse(
                question_id="",
                question_number=current_q_num,
                total_questions=total_questions,
                question_text="",
                skill_being_tested="",
                difficulty_level="",
                completed=True
            )

        # Mark as asked
        try:
            db[COLLECTION_INTERVIEWS].update_one(
                {"interview_id": interview_id},
                {"$addToSet": {"asked_question_ids": question.get("question_id")}}
            )
        except Exception:
            pass

        return NextQuestionResponse(
            question_id=question["question_id"],
            question_number=question["number"],
            total_questions=total_questions,
            question_text=question["text"],
            skill_being_tested=question["skill_tested"],
            difficulty_level=question["difficulty"],
            completed=False
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting next question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interviews/{interview_id}/submit-answer")
async def submit_answer(interview_id: str, request: SubmitAnswerRequest):
    """
    Submit answer to current question
    Agentic: AI analyzes answer quality and provides feedback
    """
    try:
        db = get_database()
        
        if db is None:
            # Development mode: update DEV_STORE and return mock analysis
            interview = DEV_STORE["interviews"].get(interview_id)
            questions = DEV_STORE["questions"].get(interview_id, [])

            # Find question in dev store to extract expected key points
            q = None
            for qq in questions:
                if qq.get("question_id") == request.question_id:
                    q = qq
                    break

            expected_kp = q.get("expected_key_points") if q else None
            analysis = get_mock_analysis(request.answer, expected_kp)

            # FIXED: store answer record with complete analysis data at top level
            answer_record = {
                "interview_id": interview_id,
                "question_id": request.question_id,
                "question_number": q.get("number") if q else 0,
                "question_text": q.get("text") if q else "",
                "answer_text": request.answer,
                "overall_score": analysis.get("overall_score", 0),  # TOP LEVEL for easy access
                "communication_quality": analysis.get("communication_quality", "adequate"),
                "technical_accuracy": analysis.get("technical_accuracy", "adequate"),
                "depth_of_knowledge": analysis.get("depth_of_knowledge", "adequate"),
                "analysis": analysis,  # Keep full analysis too
                "time_taken_seconds": request.time_taken_seconds,
                "submitted_at": datetime.utcnow()
            }

            if interview is None:
                # create minimal interview doc in dev store
                interview = interview_doc = {
                    "interview_id": interview_id,
                    "candidate_name": "Dev Candidate",
                    "role": "Developer",
                    "experience": "mid",
                    "selected_skills": [],
                    "total_questions": len(questions),
                    "current_question": 0,
                    "status": "in_progress",
                    "created_at": datetime.utcnow(),
                    "answers": [],
                    "skill_scores": {}
                }
                DEV_STORE["interviews"][interview_id] = interview

            interview = DEV_STORE["interviews"][interview_id]
            interview.setdefault("answers", []).append(answer_record)
            interview["current_question"] = interview.get("current_question", 0) + 1

            # Save structured evaluation for this answer
            interview.setdefault("evaluations", []).append(analysis)

            # Update skill score
            if q:
                skill_name = q.get("skill_tested", "General")
                skill_score = analysis.get("overall_score", 50)
                interview.setdefault("skill_scores", {})[skill_name] = skill_score

            # If we've reached the total number of questions, generate final report
            if len(interview.get("evaluations", [])) >= interview.get("total_questions", 0):
                # FIXED: Pass complete answer data with all quality metrics
                interview_data = []
                for a in interview.get("answers", []):
                    interview_data.append({
                        "question_text": a.get("question_text", ""),
                        "answer_text": a.get("answer_text", ""),
                        "overall_score": a.get("overall_score", 0),  # Direct access
                        "communication_quality": a.get("communication_quality", "adequate"),
                        "technical_accuracy": a.get("technical_accuracy", "adequate"),
                        "depth_of_knowledge": a.get("depth_of_knowledge", "adequate")
                    })
                
                report = report_generator.generate_comprehensive_report(
                    candidate_name=interview.get("candidate_name", "Dev Candidate"),
                    role=interview.get("role", "Developer"),
                    experience=interview.get("experience", "mid"),
                    selected_skills=interview.get("selected_skills", []),
                    interview_data=interview_data,  # FIXED: Complete data
                    individual_scores=interview.get("skill_scores", {})
                )
                interview["final_report"] = report

            return {
                "success": True,
                "question_id": request.question_id,
                "analysis": analysis,
                "feedback": analysis.get("feedback_to_candidate", "Good answer!")
            }
        
        # Get interview
        interview = db[COLLECTION_INTERVIEWS].find_one(
            {"interview_id": interview_id}
        )
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Get question
        question = db[COLLECTION_QUESTIONS].find_one({
            "question_id": request.question_id
        })
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Analyze answer using agentic AI
        print(f"🤖 Analyzing answer for question {question['number']}...")
        analysis = answer_analyzer.analyze_single_answer(
            question_text=question["text"],
            answer_text=request.answer,
            expected_key_points=question.get("expected_key_points", []),
            skill_tested=question["skill_tested"],
            difficulty=question["difficulty"]
        )
        
        # FIXED: Store answer with complete analysis data at top level
        answer_record = {
            "interview_id": interview_id,
            "question_id": request.question_id,
            "question_number": question["number"],
            "question_text": question["text"],
            "answer_text": request.answer,
            "overall_score": analysis.get("overall_score", 0),  # TOP LEVEL
            "communication_quality": analysis.get("communication_quality", "adequate"),
            "technical_accuracy": analysis.get("technical_accuracy", "adequate"),
            "depth_of_knowledge": analysis.get("depth_of_knowledge", "adequate"),
            "analysis": analysis,  # Keep full analysis
            "time_taken_seconds": request.time_taken_seconds,
            "submitted_at": datetime.utcnow()
        }
        
        db[COLLECTION_INTERVIEWS].update_one(
            {"interview_id": interview_id},
            {
                "$push": {"answers": answer_record},
                "$inc": {"current_question": 1}
            }
        )
        
        # Update skill scores
        skill_name = question["skill_tested"]
        skill_score = analysis.get("overall_score", 50)
        
        db[COLLECTION_INTERVIEWS].update_one(
            {"interview_id": interview_id},
            {
                "$set": {
                    f"skill_scores.{skill_name}": skill_score
                }
            }
        )

        # Append structured evaluation to interview.evaluations
        try:
            db[COLLECTION_INTERVIEWS].update_one(
                {"interview_id": interview_id},
                {"$push": {"evaluations": analysis}}
            )
        except Exception:
            pass

        # Re-fetch interview to check if all evaluations are present
        try:
            interview_after = db[COLLECTION_INTERVIEWS].find_one({"interview_id": interview_id})
            evaluations_list = interview_after.get("evaluations", []) or []
            total_q = interview_after.get("total_questions", 0)
            if len(evaluations_list) >= total_q and total_q > 0:
                # Generate final report now that all answers evaluated
                print("🤖 Generating final report (all evaluations present)...")
                answers = interview_after.get("answers", [])
                # FIXED: Pass complete answer data with all quality metrics
                interview_data = []
                for a in answers:
                    interview_data.append({
                        "question_text": a.get("question_text", ""),
                        "answer_text": a.get("answer_text", ""),
                        "overall_score": a.get("overall_score", 0),  # Direct access
                        "communication_quality": a.get("communication_quality", "adequate"),
                        "technical_accuracy": a.get("technical_accuracy", "adequate"),
                        "depth_of_knowledge": a.get("depth_of_knowledge", "adequate")
                    })
                
                report = report_generator.generate_comprehensive_report(
                    candidate_name=interview_after.get("candidate_name", "Candidate"),
                    role=interview_after.get("role", ""),
                    experience=interview_after.get("experience", ""),
                    selected_skills=interview_after.get("selected_skills", []),
                    interview_data=interview_data,  # FIXED: Complete data
                    individual_scores=interview_after.get("skill_scores", {})
                )

                # Persist report into evaluations collection and update interview
                report_doc = {
                    "interview_id": interview_id,
                    "candidate_name": interview_after.get("candidate_name"),
                    "role": interview_after.get("role"),
                    "experience": interview_after.get("experience"),
                    "selected_skills": interview_after.get("selected_skills"),
                    "report": report,
                    "generated_at": datetime.utcnow(),
                    "skill_scores": interview_after.get("skill_scores", {}),
                    "answers": answers
                }
                try:
                    db[COLLECTION_EVALUATIONS].insert_one(report_doc)
                except Exception:
                    pass

                try:
                    db[COLLECTION_INTERVIEWS].update_one(
                        {"interview_id": interview_id},
                        {"$set": {"final_report": report, "final_recommendation": report.get("recommendation", "maybe"), "overall_score": report.get("overall_score", 0)}}
                    )
                except Exception:
                    pass
        except Exception:
            pass
        
        print(f"✅ Answer analyzed. Score: {skill_score}/100")
        
        return {
            "success": True,
            "question_id": request.question_id,
            "analysis": analysis,
            "feedback": analysis.get("feedback_to_candidate", "Good answer!")
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error submitting answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interviews/{interview_id}/complete")
async def complete_interview(interview_id: str):
    """
    Complete interview and generate comprehensive report
    Agentic: Report synthesizes entire interview and makes hiring recommendation
    """
    try:
        db = get_database()
        
        if db is None:
            # Development mode: build report from DEV_STORE data
            interview = DEV_STORE["interviews"].get(interview_id)
            if not interview:
                # Fallback report when no interview found
                report = get_mock_report("Test Candidate", "Developer", 0, 
                                       interview_data=[], 
                                       individual_scores={})
                return {"success": True, "interview_id": interview_id, "report": report}

            answers = interview.get("answers", [])
            # If a final_report already exists in the interview doc, return it
            if interview.get("final_report"):
                return {"success": True, "interview_id": interview_id, "report": interview.get("final_report")}

            # FIXED: Pass complete answer data with all quality metrics
            interview_data = []
            for a in answers:
                interview_data.append({
                    "question_text": a.get("question_text", ""),
                    "answer_text": a.get("answer_text", ""),
                    "overall_score": a.get("overall_score", 0),  # Direct access
                    "communication_quality": a.get("communication_quality", "adequate"),
                    "technical_accuracy": a.get("technical_accuracy", "adequate"),
                    "depth_of_knowledge": a.get("depth_of_knowledge", "adequate")
                })

            individual_scores = interview.get("skill_scores", {})

            # Use the report generator (in dev mode this will call get_mock_report but now dynamic)
            report = report_generator.generate_comprehensive_report(
                candidate_name=interview.get("candidate_name", "Dev Candidate"),
                role=interview.get("role", "Developer"),
                experience=interview.get("experience", "mid"),
                selected_skills=interview.get("selected_skills", []),
                interview_data=interview_data,  # FIXED: Complete data
                individual_scores=individual_scores
            )

            return {"success": True, "interview_id": interview_id, "report": report}
        
        # Get interview
        interview = db[COLLECTION_INTERVIEWS].find_one({"interview_id": interview_id})

        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")

        # If final_report already exists, return it
        if interview.get("final_report"):
            return {"success": True, "interview_id": interview_id, "report": interview.get("final_report")}

        # Mark as completed
        db[COLLECTION_INTERVIEWS].update_one({"interview_id": interview_id}, {"$set": {"status": "completed"}})

        # Prepare interview data for report
        answers = interview.get("answers", [])
        # FIXED: Pass complete answer data with all quality metrics
        interview_data = []
        for a in answers:
            interview_data.append({
                "question_text": a.get("question_text", ""),
                "answer_text": a.get("answer_text", ""),
                "overall_score": a.get("overall_score", 0),  # Direct access
                "communication_quality": a.get("communication_quality", "adequate"),
                "technical_accuracy": a.get("technical_accuracy", "adequate"),
                "depth_of_knowledge": a.get("depth_of_knowledge", "adequate")
            })

        # Generate comprehensive report using agentic AI
        print(f"🤖 Generating comprehensive report...")
        report = report_generator.generate_comprehensive_report(
            candidate_name=interview["candidate_name"],
            role=interview["role"],
            experience=interview["experience"],
            selected_skills=interview["selected_skills"],
            interview_data=interview_data,  # FIXED: Complete data
            individual_scores=interview.get("skill_scores", {})
        )

        # Store report
        report_doc = {
            "interview_id": interview_id,
            "candidate_name": interview["candidate_name"],
            "role": interview["role"],
            "experience": interview["experience"],
            "selected_skills": interview["selected_skills"],
            "report": report,
            "generated_at": datetime.utcnow(),
            "skill_scores": interview.get("skill_scores", {}),
            "answers": answers  # Include all Q&A for the report
        }

        try:
            db[COLLECTION_EVALUATIONS].insert_one(report_doc)
        except Exception:
            pass

        # Update interview with evaluation
        try:
            db[COLLECTION_INTERVIEWS].update_one(
                {"interview_id": interview_id},
                {
                    "$set": {
                        "evaluation_id": str(uuid.uuid4()),
                        "final_recommendation": report.get("recommendation", "maybe"),
                        "overall_score": report.get("overall_score", 0),
                        "final_report": report
                    }
                }
            )
        except Exception:
            pass

        print(f"✅ Report generated. Recommendation: {report.get('recommendation')}")

        return {"success": True, "interview_id": interview_id, "report": report}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error completing interview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/interviews/{interview_id}/evaluation")
async def get_evaluation(interview_id: str):
    """
    Retrieve generated evaluation/report with all Q&A
    """
    try:
        db = get_database()
        
        if db is None:
            # Development mode
            report = get_mock_report("Test Candidate", "Developer", 8)
            return {
                "interview_id": interview_id,
                "candidate_name": "Test Candidate",
                "role": "Developer",
                "experience": "mid",
                "report": report,
                "skill_scores": {"React": 75, "TypeScript": 80},
                "answers": []
            }
        
        evaluation = db[COLLECTION_EVALUATIONS].find_one(
            {"interview_id": interview_id}
        )
        
        if not evaluation:
            # If a final_report was stored on the interview doc, return that as a fallback
            interview = db[COLLECTION_INTERVIEWS].find_one({"interview_id": interview_id})
            if interview and interview.get("final_report"):
                return {
                    "interview_id": interview_id,
                    "candidate_name": interview.get("candidate_name"),
                    "role": interview.get("role"),
                    "experience": interview.get("experience"),
                    "report": interview.get("final_report"),
                    "skill_scores": interview.get("skill_scores", {}),
                    "answers": interview.get("answers", [])
                }
            raise HTTPException(
                status_code=404, 
                detail="EVALUATION_NOT_FOUND: Interview not completed yet"
            )
        
        # Remove MongoDB _id field
        evaluation.pop("_id", None)
        
        return evaluation
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error retrieving evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/interviews/{interview_id}/evaluation/exists")
async def has_evaluation(interview_id: str):
    """
    Check if evaluation exists for this interview
    """
    try:
        db = get_database()
        
        if db is None:
            return {"exists": False}
        
        evaluation = db[COLLECTION_EVALUATIONS].find_one(
            {"interview_id": interview_id}
        )
        
        return {"exists": evaluation is not None}
    
    except Exception as e:
        print(f"❌ Error checking evaluation: {e}")
        return {"exists": False}


@app.get("/api/interviews/{interview_id}")
async def get_interview(interview_id: str):
    """
    Get interview details and current status
    """
    try:
        db = get_database()
        
        if db is None:
            return {
                "interview_id": interview_id,
                "candidate_name": "Test Candidate",
                "role": "Developer",
                "experience": "mid",
                "status": "in_progress",
                "current_question": 0,
                "total_questions": 8
            }
        
        interview = db[COLLECTION_INTERVIEWS].find_one(
            {"interview_id": interview_id}
        )
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Remove MongoDB _id field
        interview.pop("_id", None)
        
        # Remove sensitive data
        interview.pop("answers", None)
        
        return interview
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting interview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = get_database()
        db_status = "connected" if db is not None else "development_mode"
        
        if db is not None:
            db.command('ping')
        
        return {
            "status": "ok",
            "service": "agentic-interview-api",
            "database": db_status,
            "ai": "gemini" if not DEVELOPMENT_MODE else "development_mode"
        }
    except Exception as e:
        return {
            "status": "ok",
            "service": "agentic-interview-api",
            "database": "development_mode",
            "ai": "development_mode",
            "note": "Running in development mode"
        }


@app.get("/api/debug/questions/{interview_id}")
async def debug_questions(interview_id: str):
    """Debug endpoint to view generated questions"""
    try:
        db = get_database()
        
        if db is None:
            return {"questions": [], "note": "Development mode"}
        
        questions = list(db[COLLECTION_QUESTIONS].find(
            {"interview_id": interview_id},
            {"_id": 0}
        ))
        
        return {"questions": questions}
    
    except Exception as e:
        print(f"❌ Error fetching questions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Starting Agentic Interview AI Backend")
    print("=" * 60)
    
    if DEVELOPMENT_MODE:
        print("⚠️  DEVELOPMENT MODE ACTIVE")
        print("   - Using mock data for AI responses")
        print("   - Set GEMINI_API_KEY to enable real AI")
    else:
        print("✅ Gemini AI Integration Active")
    
    db = get_database()
    if db:
        print("✅ MongoDB Connected")
    else:
        print("⚠️  MongoDB in Development Mode")
    
    print("✅ Dynamic Question Generation")
    print("✅ AI Answer Analysis")
    print("✅ Agentic Report Generation")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )