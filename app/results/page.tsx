"use client"

import { useState, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import {
  Brain,
  TrendingUp,
  TrendingDown,
  CheckCircle2,
  AlertCircle,
  Award,
  Download,
  ArrowLeft,
} from "lucide-react"
import { getEvaluation, hasEvaluation } from "@/lib/api"

export default function ResultsPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const interviewId = searchParams.get("id")

  const [evaluation, setEvaluation] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchEvaluation = async () => {
      if (!interviewId) {
        router.push("/setup")
        return
      }

      try {
        setIsLoading(true)
        setError(null)
        
        // Check if evaluation exists first
        const exists = await hasEvaluation(interviewId)
        
        if (!exists) {
          setError("Interview not completed yet. Please complete all questions first.")
          setIsLoading(false)
          return
        }
        
        // Get the evaluation
        const result = await getEvaluation(interviewId)
        setEvaluation(result)
        
      } catch (err: any) {
        console.error("Error fetching evaluation:", err)
        
        if (err?.message?.includes("EVALUATION_NOT_FOUND")) {
          setError("Interview not completed yet. Please complete all questions first.")
        } else {
          setError(err?.message || "Failed to load evaluation report")
        }
      } finally {
        setIsLoading(false)
      }
    }

    fetchEvaluation()
  }, [interviewId, router])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="p-8 text-center">
          <Brain className="w-12 h-12 animate-pulse mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">
            Loading evaluation report...
          </p>
        </Card>
      </div>
    )
  }

  if (error || !evaluation) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="p-8 text-center max-w-md">
          <AlertCircle className="w-12 h-12 mx-auto mb-4 text-orange-500" />
          <h2 className="text-2xl font-bold mb-2">Report Not Ready</h2>
          <p className="text-muted-foreground mb-6">
            {error || "Failed to load evaluation report"}
          </p>
          <div className="flex gap-3 justify-center">
            <Button 
              onClick={() => router.push(`/interview?id=${interviewId}`)}
              variant="default"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Continue Interview
            </Button>
            <Button 
              onClick={() => router.push("/setup")}
              variant="outline"
            >
              Start New Interview
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  const report = evaluation?.report || {}
  const skillScores = evaluation?.skill_scores || {}

  // Determine recommendation color
  const getRecommendationColor = (rec: string) => {
    const recommendation = rec?.toLowerCase().replace("_", "-")
    switch (recommendation) {
      case "strong-hire":
        return "text-green-600 bg-green-50 border-green-200"
      case "hire":
        return "text-blue-600 bg-blue-50 border-blue-200"
      case "maybe":
        return "text-yellow-600 bg-yellow-50 border-yellow-200"
      case "no-hire":
      default:
        return "text-red-600 bg-red-50 border-red-200"
    }
  }

  const getRecommendationIcon = (rec: string) => {
    const recommendation = rec?.toLowerCase().replace("_", "-")
    switch (recommendation) {
      case "strong-hire":
      case "hire":
        return <CheckCircle2 className="w-8 h-8" />
      case "maybe":
        return <AlertCircle className="w-8 h-8" />
      default:
        return <AlertCircle className="w-8 h-8" />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="container mx-auto px-4 lg:px-8 py-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center">
              <Brain className="w-7 h-7 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">{evaluation?.candidate_name}</h1>
              <p className="text-muted-foreground">
                {evaluation?.role} • {evaluation?.experience} level
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 lg:px-8 py-8 max-w-5xl">
        {/* Overall Score Card */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="p-6 text-center border-2 border-primary/20">
            <div className="text-4xl font-bold text-primary mb-2">
              {Math.round(report?.overall_score || 0)}
            </div>
            <div className="text-sm text-muted-foreground">Overall Score</div>
          </Card>

          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {Math.round(report?.technical_score || 0)}
            </div>
            <div className="text-sm text-muted-foreground">Technical</div>
          </Card>

          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {Math.round(report?.communication_score || 0)}
            </div>
            <div className="text-sm text-muted-foreground">Communication</div>
          </Card>

          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-orange-600 mb-2">
              {Math.round(report?.cultural_fit_score || 0)}
            </div>
            <div className="text-sm text-muted-foreground">Culture Fit</div>
          </Card>
        </div>

        {/* Recommendation */}
        <Card className={`p-8 mb-8 text-center border-2 ${getRecommendationColor(report?.recommendation)}`}>
          <div className="flex items-center justify-center gap-3 mb-4">
            {getRecommendationIcon(report?.recommendation)}
            <h2 className="text-3xl font-bold uppercase">
              {report?.recommendation?.replace(/-|_/g, " ") || "PENDING"}
            </h2>
          </div>
          <p className="text-lg mt-4 max-w-3xl mx-auto">
            {report?.final_reasoning || "Evaluation in progress..."}
          </p>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Strengths */}
          <Card className="p-6">
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
              <TrendingUp className="text-green-600" />
              Key Strengths
            </h3>
            <ul className="space-y-3">
              {report?.strengths?.length > 0 ? (
                report.strengths.map((strength: string, idx: number) => (
                  <li key={idx} className="flex gap-2">
                    <CheckCircle2 className="text-green-600 flex-shrink-0 mt-0.5 w-5 h-5" />
                    <span className="text-sm">{strength}</span>
                  </li>
                ))
              ) : (
                <li className="text-muted-foreground text-sm">No strengths recorded</li>
              )}
            </ul>
          </Card>

          {/* Development Areas */}
          <Card className="p-6">
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
              <TrendingDown className="text-orange-600" />
              Development Areas
            </h3>
            <ul className="space-y-3">
              {report?.development_areas?.length > 0 ? (
                report.development_areas.map((area: string, idx: number) => (
                  <li key={idx} className="flex gap-2">
                    <AlertCircle className="text-orange-600 flex-shrink-0 mt-0.5 w-5 h-5" />
                    <span className="text-sm">{area}</span>
                  </li>
                ))
              ) : (
                <li className="text-muted-foreground text-sm">No development areas</li>
              )}
            </ul>
          </Card>
        </div>

        {/* Skill Scores */}
        {Object.keys(skillScores).length > 0 && (
          <Card className="p-6 mb-8">
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Award className="text-blue-600" />
              Skill Assessment
            </h3>
            <div className="space-y-4">
              {Object.entries(skillScores).map(([skill, score]: [string, any]) => (
                <div key={skill}>
                  <div className="flex justify-between mb-2">
                    <span className="font-medium">{skill}</span>
                    <span className="text-sm font-semibold">{Math.round(score)}/100</span>
                  </div>
                  <Progress value={score} className="h-2" />
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Role Fit Assessment */}
        {report?.role_fit_assessment && (
          <Card className="p-6 mb-8">
            <h3 className="text-xl font-bold mb-4">Role Fit Assessment</h3>
            <p className="text-muted-foreground leading-relaxed">
              {report.role_fit_assessment}
            </p>
          </Card>
        )}

        {/* 3-Month Development Plan */}
        {report?.three_month_plan?.length > 0 && (
          <Card className="p-6 mb-8">
            <h3 className="text-xl font-bold mb-4">3-Month Development Plan</h3>
            <ol className="space-y-3 list-decimal list-inside">
              {report.three_month_plan.map((goal: string, idx: number) => (
                <li key={idx} className="text-muted-foreground leading-relaxed">
                  {goal}
                </li>
              ))}
            </ol>
          </Card>
        )}

        {/* Next Round Questions (if available) */}
        {report?.next_round_questions?.length > 0 && (
          <Card className="p-6 mb-8 border-blue-200 bg-blue-50">
            <h3 className="text-xl font-bold mb-4">Suggested Follow-up Questions</h3>
            <ul className="space-y-2">
              {report.next_round_questions.map((question: string, idx: number) => (
                <li key={idx} className="flex gap-2">
                  <span className="text-blue-600 font-semibold flex-shrink-0">Q{idx + 1}:</span>
                  <span className="text-muted-foreground">{question}</span>
                </li>
              ))}
            </ul>
          </Card>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center">
          <Button
            onClick={() => router.push("/setup")}
            variant="default"
            size="lg"
          >
            Start New Interview
          </Button>
          <Button
            onClick={() => window.print()}
            variant="outline"
            size="lg"
            className="gap-2"
          >
            <Download className="w-4 h-4" />
            Print Report
          </Button>
        </div>
      </main>
    </div>
  )
}