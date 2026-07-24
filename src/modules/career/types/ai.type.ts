export interface OptimizeDescriptionData {
  text: string
  targetRole?: string | null
  seniorityLevel?: string | null
}

export interface OptimizeDescriptionResult {
  optimizedText: string
}

export interface SuggestResponsibilitiesData {
  roleCategory: string
  seniorityLevel?: string | null
}

export interface SuggestResponsibilitiesResult {
  suggestions: string[]
  source: 'library' | 'ai'
}

export interface AnalyzeProfileResult {
  matchScore: number
  strengths: string[]
  gaps: string[]
  recommendations: string[]
}

export interface ICareerAiService {
  optimizeDescription(data: OptimizeDescriptionData): Promise<OptimizeDescriptionResult>
  suggestResponsibilities(data: SuggestResponsibilitiesData): Promise<SuggestResponsibilitiesResult>
  analyzeProfile(targetRole: string): Promise<AnalyzeProfileResult>
}
