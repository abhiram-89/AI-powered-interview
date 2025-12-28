import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Brain,
  Sparkles,
  Target,
  TrendingUp,
  Users,
  Zap,
  MessageSquare,
  BarChart3,
  CheckCircle2,
  ArrowRight,
} from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Brain className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-semibold text-xl text-foreground">AI Interview</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Features
            </Link>
            <Link
              href="#how-it-works"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              How it Works
            </Link>
            <Link href="#benefits" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Benefits
            </Link>
          </nav>
          <Button asChild>
            <Link href="/setup">Get Started</Link>
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 lg:px-8 py-20 lg:py-32">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <Badge variant="secondary" className="px-4 py-1.5 text-sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 inline-block" />
            Powered by Advanced AI
          </Badge>
          <h1 className="text-5xl lg:text-7xl font-bold tracking-tight text-balance">
            The fastest platform for <span className="text-primary">AI-powered interviews</span>
          </h1>
          <p className="text-xl text-muted-foreground leading-relaxed text-pretty max-w-2xl mx-auto">
            Build transformative hiring experiences with adaptive interviews, real-time evaluation, and intelligent
            candidate screening.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Button size="lg" className="text-base px-8" asChild>
              <Link href="/setup">
                Start Interview <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" className="text-base px-8 bg-transparent" asChild>
              <Link href="/demo">View Demo</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {[
            { value: "90%", label: "Time saved on evaluation", icon: TrendingUp },
            { value: "5x", label: "Faster screening process", icon: Zap },
            { value: "95%", label: "Interview accuracy", icon: Target },
            { value: "1000+", label: "Interviews conducted", icon: Users },
          ].map((stat, idx) => (
            <Card key={idx} className="p-6 text-center border-border bg-card hover:shadow-lg transition-all">
              <stat.icon className="w-8 h-8 mx-auto mb-3 text-primary" />
              <div className="text-3xl font-bold text-foreground mb-1">{stat.value}</div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </Card>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 lg:px-8 py-20 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-balance">Everything you need for smart hiring</h2>
            <p className="text-lg text-muted-foreground text-pretty">
              Comprehensive AI-powered tools for conducting and evaluating technical interviews
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                icon: Brain,
                title: "Adaptive Questioning",
                description: "AI adjusts question difficulty based on candidate responses in real-time",
              },
              {
                icon: MessageSquare,
                title: "Natural Conversation",
                description: "Interactive chat interface that feels like talking to a real interviewer",
              },
              {
                icon: BarChart3,
                title: "Instant Evaluation",
                description: "Get comprehensive skill scores and detailed performance analysis",
              },
              {
                icon: Target,
                title: "Role-Specific Questions",
                description: "Tailored questions for Frontend, Backend, Data Science, and more",
              },
              {
                icon: Sparkles,
                title: "AI-Generated Reports",
                description: "Structured evaluation reports with strengths and improvement areas",
              },
              {
                icon: CheckCircle2,
                title: "Hire Recommendations",
                description: "Data-driven hiring decisions based on comprehensive candidate assessment",
              },
            ].map((feature, idx) => (
              <Card key={idx} className="p-6 border-border bg-card hover:shadow-lg transition-all group">
                <feature.icon className="w-10 h-10 text-primary mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-xl font-semibold mb-2 text-foreground">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="container mx-auto px-4 lg:px-8 py-20">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-balance">How it works</h2>
            <p className="text-lg text-muted-foreground text-pretty">
              Simple, effective interview process in five steps
            </p>
          </div>
          <div className="space-y-8">
            {[
              {
                step: "01",
                title: "Interview Setup",
                description: "Select role type, experience level, and required skills for the position",
              },
              {
                step: "02",
                title: "AI Question Generation",
                description: "AI generates technical, scenario-based, and follow-up questions tailored to the role",
              },
              {
                step: "03",
                title: "Adaptive Interview",
                description:
                  "AI adjusts difficulty dynamically - simpler questions for weak answers, advanced for strong ones",
              },
              {
                step: "04",
                title: "Real-time Evaluation",
                description: "AI evaluates technical correctness, clarity, and problem-solving approach instantly",
              },
              {
                step: "05",
                title: "Comprehensive Report",
                description:
                  "Generate detailed reports with skill scores, strengths, weaknesses, and hiring recommendations",
              },
            ].map((item, idx) => (
              <div key={idx} className="flex gap-6 items-start">
                <div className="flex-shrink-0 w-16 h-16 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-2xl font-bold">
                  {item.step}
                </div>
                <div className="flex-1 pt-2">
                  <h3 className="text-2xl font-semibold mb-2 text-foreground">{item.title}</h3>
                  <p className="text-muted-foreground leading-relaxed text-lg">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="container mx-auto px-4 lg:px-8 py-20 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-balance">Why use AI Interview Assistant</h2>
            <p className="text-lg text-muted-foreground text-pretty">
              Transform your hiring process with intelligent automation
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                title: "Save Time",
                description: "Reduce interview evaluation time by 90% with automated AI assessment and instant reports",
                benefit: "Hours saved per candidate",
              },
              {
                title: "Improve Quality",
                description: "Consistent, bias-free evaluation criteria ensures fair assessment for all candidates",
                benefit: "Better hiring decisions",
              },
              {
                title: "Scale Efficiently",
                description: "Conduct multiple interviews simultaneously without compromising on quality or depth",
                benefit: "Unlimited scalability",
              },
              {
                title: "Data-Driven Insights",
                description: "Comprehensive analytics and skill mapping help identify the best talent for your team",
                benefit: "Smarter decisions",
              },
            ].map((item, idx) => (
              <Card key={idx} className="p-8 border-border bg-card hover:shadow-lg transition-all">
                <Badge variant="secondary" className="mb-4">
                  {item.benefit}
                </Badge>
                <h3 className="text-2xl font-semibold mb-3 text-foreground">{item.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{item.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 lg:px-8 py-20">
        <Card className="max-w-4xl mx-auto p-12 text-center bg-primary text-primary-foreground border-0">
          <h2 className="text-4xl font-bold mb-4 text-balance">Ready to transform your hiring?</h2>
          <p className="text-xl mb-8 text-primary-foreground/90 text-pretty">
            Start conducting intelligent interviews in minutes
          </p>
          <Button size="lg" variant="secondary" className="text-base px-8" asChild>
            <Link href="/setup">
              Start Your First Interview <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </Button>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12">
        <div className="container mx-auto px-4 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-primary flex items-center justify-center">
                <Brain className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">AI Interview Assistant</span>
            </div>
            <p className="text-sm text-muted-foreground">Built with React, FastAPI, and Advanced AI</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
