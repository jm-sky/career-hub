import type { Technology } from '@/modules/career/types/technology.type'

// Free-form text, up to 30 chars — matches the backend column, not a fixed set of options.
export interface Experience {
  id: string
  profileId: string
  companyName: string
  position: string
  employmentType: string | null
  startDate: string
  endDate: string | null
  isCurrent: boolean
  description: string | null
  responsibilities: string[]
  displayOrder: number
  technologies: Technology[]
  createdAt: string
  updatedAt: string
}

export interface CreateExperienceData {
  companyName: string
  position: string
  employmentType?: string | null
  startDate: string
  endDate?: string | null
  isCurrent?: boolean
  description?: string | null
  responsibilities?: string[]
  technologies?: string[]
}

export interface UpdateExperienceData {
  companyName?: string
  position?: string
  employmentType?: string | null
  startDate?: string
  endDate?: string | null
  isCurrent?: boolean
  description?: string | null
  responsibilities?: string[]
  technologies?: string[]
}

export interface IExperienceService {
  list(): Promise<Experience[]>
  create(data: CreateExperienceData): Promise<Experience>
  update(id: string, data: UpdateExperienceData): Promise<Experience>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Experience[]>
}
