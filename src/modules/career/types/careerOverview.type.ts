import type { ProfileVisibility } from '@/modules/career/types/profile.type'

export interface CareerSectionCounts {
  experiences: number
  projects: number
  skills: number
  education: number
  certifications: number
  achievements: number
  languages: number
  cvVersions: number
}

export interface CareerOverview {
  slug: string
  headline: string | null
  visibility: ProfileVisibility
  profileCompleteness: number
  completenessScore: number
  counts: CareerSectionCounts
  suggestions: string[]
}

export interface ICareerOverviewService {
  getOverview(): Promise<CareerOverview>
}
