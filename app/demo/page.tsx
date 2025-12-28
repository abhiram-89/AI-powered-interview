"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, ArrowLeft, Play, FileText, MessageSquare, BarChart3 } from "lucide-react"

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur">
        <div className="container mx-auto px-4 lg:px-8 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <ArrowLeft className="w-4 h-4 text-muted-foreground" />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                <Brain className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="font-semibold text-xl text-foreground">AI Interview</span>
            </div>
          </Link>
          <Badge variant="outline" className="text-sm">
            Demo Mode
          </Badge>
        </div>
      </header>

      <div className="container mx-auto px-4 lg:px-8 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4 text-foreground text-balance">Experience the Demo</h1>
            <p className="text-xl text-muted-foreground text-pretty">
              See how our AI-powered interview system works in action
            </p>
          </div>

          <div className="grid gap-6 mb-12">
            <Card className="p-8 hover:shadow-lg transition-all">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <FileText className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2 text-foreground">1. Interview Setup</h3>
                  <p className="text-muted-foreground leading-relaxed mb-4">
                    Configure your interview by selecting the role, experience level, and required skills. Our intuitive
                    wizard makes setup quick and easy.
                  </p>
                  <Button asChild>
                    <Link href="/setup">
                      <Play className="w-4 h-4 mr-2" />
                      Try Setup Flow
                    </Link>
                  </Button>
                </div>
              </div>
            </Card>

            <Card className="p-8 hover:shadow-lg transition-all">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <MessageSquare className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2 text-foreground">2. Interactive Interview</h3>
                  <p className="text-muted-foreground leading-relaxed mb-4">
                    Engage in a natural conversation with our AI interviewer. Questions adapt based on your responses,
                    creating a personalized experience.
                  </p>
                  <Badge variant="secondary">Coming Soon in Demo</Badge>
                </div>
              </div>
            </Card>

            <Card className="p-8 hover:shadow-lg transition-all">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <BarChart3 className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2 text-foreground">3. Comprehensive Results</h3>
                  <p className="text-muted-foreground leading-relaxed mb-4">
                    Get detailed evaluation reports with skill scores, strengths, areas for improvement, and hiring
                    recommendations.
                  </p>
                  <Button variant="outline" asChild>
                    <Link href="/results">
                      <Play className="w-4 h-4 mr-2" />
                      View Sample Report
                    </Link>
                  </Button>
                </div>
              </div>
            </Card>
          </div>

          <Card className="p-8 text-center bg-primary text-primary-foreground border-0">
            <h2 className="text-2xl font-bold mb-4 text-balance">Ready to start your own interview?</h2>
            <p className="text-lg mb-6 text-primary-foreground/90 text-pretty">
              Experience the full platform with real AI-powered interviews
            </p>
            <Button size="lg" variant="secondary" asChild>
              <Link href="/setup">Get Started Now</Link>
            </Button>
          </Card>
        </div>
      </div>
    </div>
  )
}
