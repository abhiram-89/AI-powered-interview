/**
 * API Client for Agentic Interview Platform
 * Handles all communication with the FastAPI backend
 * 
 * Place this file at: lib/api.ts in your Next.js project
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * Helper function to handle API responses
 */
async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new Error(error.detail || `API Error: ${response.status}`)
  }
  return response.json()
}

/**
 * Create a new interview session
 */
export async function createInterview(data: {
  candidate_name: string
  role: string
  experience: string
  selected_skills: Array<{
    skill_name: string
    proficiency_level: string
    experience_years?: number
  }>
  interview_duration_minutes?: number
}) {
  const response = await fetch(`${API_BASE_URL}/api/interviews/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
  
  return handleResponse(response)
}

/**
 * Get interview details
 */
export async function getInterview(interviewId: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/interviews/${interviewId}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  
  return handleResponse(response)
}

/**
 * Get the next question in the interview
 */
export async function getNextQuestion(interviewId: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/interviews/${interviewId}/next-question`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  
  return handleResponse(response)
}

/**
 * Submit an answer to a question
 */
export async function submitResponse(
  interviewId: string,
  questionId: string,
  answer: string,
  timeTakenSeconds: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/interviews/${interviewId}/submit-answer`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question_id: questionId,
        answer: answer,
        time_taken_seconds: timeTakenSeconds,
      }),
    }
  )
  
  return handleResponse(response)
}

/**
 * Complete the interview and generate report
 */
export async function completeInterview(interviewId: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/interviews/${interviewId}/complete`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  
  return handleResponse(response)
}

/**
 * Get the evaluation report
 */
export async function getEvaluation(interviewId: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/interviews/${interviewId}/evaluation`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  
  return handleResponse(response)
}

/**
 * Check if evaluation exists
 */
export async function hasEvaluation(interviewId: string): Promise<boolean> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/interviews/${interviewId}/evaluation/exists`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    
    const data = await handleResponse(response)
    return data.exists
  } catch (error) {
    console.error("Error checking evaluation existence:", error)
    return false
  }
}

/**
 * Health check
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  
  return handleResponse(response)
}

/**
 * Debug: Get all questions for an interview
 */
export async function getDebugQuestions(interviewId: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/debug/questions/${interviewId}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  
  return handleResponse(response)
}