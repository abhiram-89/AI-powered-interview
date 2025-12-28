"use client"

import { useState, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import {
  Brain,
  CheckCircle2,
  Clock,
  MessageSquare,
  Sparkles,
} from "lucide-react"
import {
  getInterview,
  getNextQuestion,
  submitResponse,
  completeInterview,
} from "@/lib/api"

export default function InterviewPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const interviewId = searchParams.get("id")

  // Interview state
  const [interview, setInterview] = useState<any>(null)
  const [currentQuestion, setCurrentQuestion] = useState<any>(null)
  const [answer, setAnswer] = useState("")
  const [feedback, setFeedback] = useState<any>(null)

  // UI state
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isCompleting, setIsCompleting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [startTime, setStartTime] = useState<number>(Date.now())

  // Load interview and first question
  useEffect(() => {
    const initializeInterview = async () => {
      if (!interviewId) {
        router.push("/setup")
        return
      }

      try {
        setIsLoading(true)
        
        // Get interview details
        const interviewData = await getInterview(interviewId)
        setInterview(interviewData)

        // Get first question
        const question = await getNextQuestion(interviewId)
        
        if (question.completed) {
          // No more questions - this shouldn't happen on first load
          router.push(`/results?id=${interviewId}`)
          return
        }

        setCurrentQuestion(question)
        setStartTime(Date.now())
        
      } catch (err: any) {
        console.error("Error initializing interview:", err)
        setError(err?.message || "Failed to start interview")
      } finally {
        setIsLoading(false)
      }
    }

    initializeInterview()
  }, [interviewId, router])

  // Handle answer submission
  const handleSubmitAnswer = async () => {
    if (!answer.trim()) {
      setError("Please provide an answer")
      return
    }

    try {
      setIsSubmitting(true)
      setError(null)

      // Calculate time taken
      const timeTaken = Math.floor((Date.now() - startTime) / 1000)

      // Submit answer
      const result = await submitResponse(
        interviewId!,
        currentQuestion.question_id,
        answer,
        timeTaken
      )

      // Show feedback briefly
      setFeedback(result)

      // Wait 2 seconds to show feedback, then load next question
      setTimeout(async () => {
        try {
          // Get next question
          const nextQuestion = await getNextQuestion(interviewId!)

          if (nextQuestion.completed) {
            // Interview is complete - generate report
            await handleCompleteInterview()
          } else {
            // Load next question
            setCurrentQuestion(nextQuestion)
            setAnswer("")
            setFeedback(null)
            setStartTime(Date.now())
          }
        } catch (err: any) {
          console.error("Error loading next question:", err)
          setError(err?.message || "Failed to load next question")
        } finally {
          setIsSubmitting(false)
        }
      }, 2000)

    } catch (err: any) {
      console.error("Error submitting answer:", err)
      setError(err?.message || "Failed to submit answer")
      setIsSubmitting(false)
    }
  }

  // Handle interview completion
  const handleCompleteInterview = async () => {
    try {
      setIsCompleting(true)

      // Complete interview and generate report
      await completeInterview(interviewId!)

      // Navigate to results page
      router.push(`/results?id=${interviewId}`)

    } catch (err: any) {
      console.error("Error completing interview:", err)
      setError(err?.message || "Failed to complete interview")
      setIsCompleting(false)
    }
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="p-8 text-center">
          <Brain className="w-12 h-12 animate-pulse mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">
            Loading interview...
          </p>
        </Card>
      </div>
    )
  }

  // Completing state
  if (isCompleting) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="p-8 text-center max-w-md">
          <Sparkles className="w-12 h-12 animate-pulse mx-auto mb-4 text-primary" />
          <h2 className="text-2xl font-bold mb-2">Generating Report</h2>
          <p className="text-muted-foreground mb-4">
            Our AI is analyzing your responses and creating a comprehensive evaluation...
          </p>
          <div className="animate-pulse flex gap-2 justify-center">
            <div className="w-2 h-2 bg-primary rounded-full"></div>
            <div className="w-2 h-2 bg-primary rounded-full"></div>
            <div className="w-2 h-2 bg-primary rounded-full"></div>
          </div>
        </Card>
      </div>
    )
  }

  // Error state
  if (error && !currentQuestion) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="p-8 text-center max-w-md">
          <div className="text-red-500 mb-4">Error</div>
          <p className="text-muted-foreground mb-4">{error}</p>
          <Button onClick={() => router.push("/setup")}>
            Start New Interview
          </Button>
        </Card>
      </div>
    )
  }

  // Main interview UI
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="container mx-auto px-4 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                <Brain className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold">{interview?.candidate_name}</h1>
                <p className="text-sm text-muted-foreground">
                  {interview?.role} • {interview?.experience}
                </p>
              </div>
            </div>

            {/* Progress */}
            {currentQuestion && (
              <div className="text-right">
                <div className="text-sm font-medium mb-1">
                  Question {currentQuestion.question_number} of {currentQuestion.total_questions}
                </div>
                <Progress 
                  value={(currentQuestion.question_number / currentQuestion.total_questions) * 100} 
                  className="w-32 h-2"
                />
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 lg:px-8 py-8 max-w-4xl">
        {/* Question Card */}
        {currentQuestion && (
          <Card className="p-8 mb-6">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                <MessageSquare className="w-6 h-6 text-primary" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-3">
                  <Badge variant="secondary">
                    {currentQuestion.skill_being_tested}
                  </Badge>
                  <Badge variant="outline">
                    {currentQuestion.difficulty_level}
                  </Badge>
                </div>
                <p className="text-lg leading-relaxed">
                  {currentQuestion.question_text}
                </p>
              </div>
            </div>

            {/* Answer Input */}
            {!feedback && (
              <div className="space-y-4">
                <Textarea
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  className="min-h-[200px] text-base"
                  disabled={isSubmitting}
                />

                {error && (
                  <div className="text-red-500 text-sm">{error}</div>
                )}

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    <span>Time: {Math.floor((Date.now() - startTime) / 1000)}s</span>
                  </div>

                  <Button
                    onClick={handleSubmitAnswer}
                    disabled={isSubmitting || !answer.trim()}
                    size="lg"
                  >
                    {isSubmitting ? (
                      <>
                        <Brain className="w-4 h-4 mr-2 animate-pulse" />
                        Analyzing...
                      </>
                    ) : (
                      "Submit Answer"
                    )}
                  </Button>
                </div>
              </div>
            )}

            {/* Feedback */}
            {feedback && (
              <div className="space-y-4">
                <div className="flex items-start gap-3 p-4 bg-primary/5 rounded-lg">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="font-medium mb-1">AI Feedback</div>
                    <p className="text-sm text-muted-foreground">
                      {feedback.feedback}
                    </p>
                    <div className="mt-2 text-sm">
                      <span className="font-medium">Score: </span>
                      <span className="text-primary font-bold">
                        {Math.round(feedback.analysis.overall_score)}/100
                      </span>
                    </div>
                  </div>
                </div>

                <div className="text-center text-sm text-muted-foreground">
                  Loading next question...
                </div>
              </div>
            )}
          </Card>
        )}

        {/* Tips Card */}
        <Card className="p-6 bg-blue-50 border-blue-200">
          <h3 className="font-medium mb-2">💡 Interview Tips</h3>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• Be specific and provide examples</li>
            <li>• Explain your reasoning clearly</li>
            <li>• Take your time to think through your answer</li>
            <li>• Mention relevant technologies and best practices</li>
          </ul>
        </Card>
      </main>
    </div>
  )
}