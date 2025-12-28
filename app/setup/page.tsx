"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Brain, ArrowLeft, ArrowRight, CheckCircle2, Loader2 } from "lucide-react"
import Link from "next/link"
import { createInterview } from "@/lib/api"

const roles = [
  { value: "frontend", label: "Frontend Developer", description: "React, Vue, Angular, UI/UX" },
  { value: "backend", label: "Backend Developer", description: "APIs, Databases, Server-side" },
  { value: "fullstack", label: "Full Stack Developer", description: "Frontend + Backend" },
  { value: "data", label: "Data Scientist", description: "ML, Analytics, Python" },
  { value: "devops", label: "DevOps Engineer", description: "CI/CD, Cloud, Infrastructure" },
  { value: "mobile", label: "Mobile Developer", description: "iOS, Android, React Native" },
]

const experienceLevels = [
  { value: "junior", label: "Junior", years: "0-2 years", description: "Entry-level position" },
  { value: "mid", label: "Mid-Level", years: "2-5 years", description: "Intermediate experience" },
  { value: "senior", label: "Senior", years: "5-8 years", description: "Advanced expertise" },
  { value: "lead", label: "Lead/Principal", years: "8+ years", description: "Leadership role" },
]

const skillsByRole = {
  frontend: ["React", "TypeScript", "CSS/Tailwind", "State Management", "Performance", "Accessibility"],
  backend: ["Node.js", "Databases", "APIs", "Security", "Scalability", "Testing"],
  fullstack: ["Frontend Frameworks", "Backend APIs", "Databases", "DevOps", "Architecture", "Testing"],
  data: ["Python", "Machine Learning", "Statistics", "Data Visualization", "SQL", "Big Data"],
  devops: ["Docker", "Kubernetes", "CI/CD", "AWS/Cloud", "Monitoring", "Infrastructure as Code"],
  mobile: ["Swift/Kotlin", "React Native", "Mobile UI", "App Store", "Push Notifications", "Performance"],
}

export default function SetupPage() {
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [candidateName, setCandidateName] = useState("")
  const [candidateEmail, setCandidateEmail] = useState("")
  const [role, setRole] = useState("")
  const [experience, setExperience] = useState("")
  const [selectedSkills, setSelectedSkills] = useState<string[]>([])
  const [duration, setDuration] = useState("30")
  const [isCreating, setIsCreating] = useState(false)

  const handleSkillToggle = (skill: string) => {
    setSelectedSkills((prev) => (prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]))
  }

  const handleStartInterview = async () => {
    setIsCreating(true)
    try {
      const roleMap: Record<string, string> = {
        frontend: "Frontend Developer",
        backend: "Backend Developer",
        fullstack: "Full Stack Developer",
        data: "Data Scientist",
        devops: "DevOps Engineer",
        mobile: "Mobile Developer",
      }

      // Build SkillSelection objects expected by backend
      const skillSelections = selectedSkills.map((s) => ({
        skill_name: s,
        proficiency_level: "intermediate",
        experience_years: undefined,
      }))

      const response = await createInterview({
        candidate_name: candidateName,
        role: roleMap[role] || role,
        experience: experience,
        selected_skills: skillSelections,
        interview_duration_minutes: Number.parseInt(duration),
      })

      localStorage.setItem("currentInterviewId", response.interview_id)
      router.push(`/interview?id=${response.interview_id}`)
    } catch (error) {
      alert("Failed to create interview. Using development mode with mock data.")
      const mockId = `interview_${Date.now()}`
      localStorage.setItem("currentInterviewId", mockId)
      router.push(`/interview?id=${mockId}`)
    } finally {
      setIsCreating(false)
    }
  }

  const canProceedStep1 = candidateName.trim() !== "" && candidateEmail.trim() !== "" && role !== ""
  const canProceedStep2 = experience !== "" && selectedSkills.length >= 2
  const canStartInterview = duration !== ""

  return (
    <div className="min-h-screen bg-background">
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
            Setup Interview
          </Badge>
        </div>
      </header>

      <div className="container mx-auto px-4 lg:px-8 py-12">
        <div className="max-w-3xl mx-auto">
          <div className="mb-12">
            <div className="flex items-center justify-between mb-4">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center flex-1">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                      s < step
                        ? "bg-primary text-primary-foreground"
                        : s === step
                          ? "bg-primary text-primary-foreground ring-4 ring-primary/20"
                          : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {s < step ? <CheckCircle2 className="w-5 h-5" /> : s}
                  </div>
                  {s < 3 && (
                    <div className={`flex-1 h-1 mx-2 transition-colors ${s < step ? "bg-primary" : "bg-muted"}`} />
                  )}
                </div>
              ))}
            </div>
            <div className="flex justify-between text-sm">
              <span className={step >= 1 ? "text-foreground font-medium" : "text-muted-foreground"}>Basic Info</span>
              <span className={step >= 2 ? "text-foreground font-medium" : "text-muted-foreground"}>
                Skills & Level
              </span>
              <span className={step >= 3 ? "text-foreground font-medium" : "text-muted-foreground"}>Final Setup</span>
            </div>
          </div>

          {step === 1 && (
            <Card className="p-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div>
                <h2 className="text-3xl font-bold mb-2 text-foreground">Basic Information</h2>
                <p className="text-muted-foreground">Let's start with the candidate details and role</p>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="candidateName" className="text-base">
                    Candidate Name
                  </Label>
                  <Input
                    id="candidateName"
                    placeholder="Enter candidate's full name"
                    value={candidateName}
                    onChange={(e) => setCandidateName(e.target.value)}
                    className="text-base"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="candidateEmail" className="text-base">
                    Email Address
                  </Label>
                  <Input
                    id="candidateEmail"
                    type="email"
                    placeholder="candidate@example.com"
                    value={candidateEmail}
                    onChange={(e) => setCandidateEmail(e.target.value)}
                    className="text-base"
                  />
                </div>

                <div className="space-y-2">
                  <Label className="text-base">Select Role</Label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {roles.map((r) => (
                      <Card
                        key={r.value}
                        className={`p-4 cursor-pointer transition-all hover:shadow-md ${
                          role === r.value
                            ? "border-primary bg-primary/5 ring-2 ring-primary"
                            : "border-border hover:border-primary/50"
                        }`}
                        onClick={() => setRole(r.value)}
                      >
                        <div className="font-semibold text-foreground mb-1">{r.label}</div>
                        <div className="text-sm text-muted-foreground">{r.description}</div>
                      </Card>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <Button size="lg" onClick={() => setStep(2)} disabled={!canProceedStep1} className="min-w-32">
                  Next <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </Card>
          )}

          {step === 2 && (
            <Card className="p-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div>
                <h2 className="text-3xl font-bold mb-2 text-foreground">Experience & Skills</h2>
                <p className="text-muted-foreground">Choose experience level and required skills</p>
              </div>

              <div className="space-y-6">
                <div className="space-y-2">
                  <Label className="text-base">Experience Level</Label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {experienceLevels.map((level) => (
                      <Card
                        key={level.value}
                        className={`p-4 cursor-pointer transition-all hover:shadow-md ${
                          experience === level.value
                            ? "border-primary bg-primary/5 ring-2 ring-primary"
                            : "border-border hover:border-primary/50"
                        }`}
                        onClick={() => setExperience(level.value)}
                      >
                        <div className="font-semibold text-foreground mb-1">{level.label}</div>
                        <div className="text-sm text-muted-foreground mb-1">{level.years}</div>
                        <div className="text-xs text-muted-foreground">{level.description}</div>
                      </Card>
                    ))}
                  </div>
                </div>

                {role && (
                  <div className="space-y-2">
                    <Label className="text-base">
                      Required Skills <span className="text-muted-foreground text-sm">(select at least 2)</span>
                    </Label>
                    <div className="flex flex-wrap gap-2">
                      {skillsByRole[role as keyof typeof skillsByRole]?.map((skill) => (
                        <Badge
                          key={skill}
                          variant={selectedSkills.includes(skill) ? "default" : "outline"}
                          className="cursor-pointer px-4 py-2 text-sm hover:shadow-md transition-all"
                          onClick={() => handleSkillToggle(skill)}
                        >
                          {selectedSkills.includes(skill) && <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" />}
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex justify-between pt-4">
                <Button size="lg" variant="outline" onClick={() => setStep(1)} className="min-w-32">
                  <ArrowLeft className="w-4 h-4 mr-2" /> Back
                </Button>
                <Button size="lg" onClick={() => setStep(3)} disabled={!canProceedStep2} className="min-w-32">
                  Next <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </Card>
          )}

          {step === 3 && (
            <Card className="p-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div>
                <h2 className="text-3xl font-bold mb-2 text-foreground">Final Setup</h2>
                <p className="text-muted-foreground">Review and configure interview duration</p>
              </div>

              <div className="space-y-6">
                <div className="p-6 bg-muted/50 rounded-lg space-y-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Candidate:</span>
                    <span className="font-semibold text-foreground">{candidateName}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Role:</span>
                    <span className="font-semibold text-foreground">{roles.find((r) => r.value === role)?.label}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Experience:</span>
                    <span className="font-semibold text-foreground">
                      {experienceLevels.find((l) => l.value === experience)?.label}
                    </span>
                  </div>
                  <div className="flex justify-between items-start">
                    <span className="text-muted-foreground">Skills:</span>
                    <div className="flex flex-wrap gap-1 justify-end max-w-xs">
                      {selectedSkills.map((skill) => (
                        <Badge key={skill} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="duration" className="text-base">
                    Interview Duration
                  </Label>
                  <Select value={duration} onValueChange={setDuration}>
                    <SelectTrigger id="duration" className="text-base">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="15">15 minutes - Quick Screening</SelectItem>
                      <SelectItem value="30">30 minutes - Standard Interview</SelectItem>
                      <SelectItem value="45">45 minutes - In-depth Interview</SelectItem>
                      <SelectItem value="60">60 minutes - Comprehensive Assessment</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex justify-between pt-4">
                <Button size="lg" variant="outline" onClick={() => setStep(2)} className="min-w-32">
                  <ArrowLeft className="w-4 h-4 mr-2" /> Back
                </Button>
                <Button
                  size="lg"
                  onClick={handleStartInterview}
                  disabled={!canStartInterview || isCreating}
                  className="min-w-40"
                >
                  {isCreating ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    <>
                      Start Interview <ArrowRight className="w-4 h-4 ml-2" />
                    </>
                  )}
                </Button>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
