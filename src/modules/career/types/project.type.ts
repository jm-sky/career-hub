import type { ProfileVisibility } from '@/modules/career/types/profile.type'
import type { Technology } from '@/modules/career/types/technology.type'

export type ProjectStatus = 'ACTIVE' | 'STAGING' | 'ARCHIVED'
export type ProjectCategory = 'DEMO' | 'INTERNAL' | 'PRODUCTION'

export interface ProjectLinks {
  demo?: string | null
  github?: string | null
  docs?: string | null
}

export interface SubProject {
  name: string
  url?: string | null
}

export interface Project {
  id: string
  profileId: string
  name: string
  description: string | null
  role: string | null
  startDate: string
  endDate: string | null
  isOngoing: boolean
  isAnonymized: boolean
  anonymizedCompany: string | null
  status: ProjectStatus
  category: ProjectCategory | null
  achievements: string[]
  challenges: string[]
  clients: string[]
  team: string[]
  subProjects: SubProject[]
  teamSize: number | null
  durationMonths: number | null
  usersCount: number | null
  budgetRange: string | null
  links: ProjectLinks
  visibility: ProfileVisibility
  displayOrder: number
  technologies: Technology[]
  experienceIds: string[]
  createdAt: string
  updatedAt: string
}

export interface CreateProjectData {
  name: string
  description?: string | null
  role?: string | null
  startDate: string
  endDate?: string | null
  isOngoing?: boolean
  isAnonymized?: boolean
  anonymizedCompany?: string | null
  status?: ProjectStatus
  category?: ProjectCategory | null
  achievements?: string[]
  challenges?: string[]
  clients?: string[]
  team?: string[]
  subProjects?: SubProject[]
  teamSize?: number | null
  durationMonths?: number | null
  usersCount?: number | null
  budgetRange?: string | null
  links?: ProjectLinks
  visibility?: ProfileVisibility
  technologies?: string[]
  experienceIds?: string[]
}

export interface UpdateProjectData {
  name?: string
  description?: string | null
  role?: string | null
  startDate?: string
  endDate?: string | null
  isOngoing?: boolean
  isAnonymized?: boolean
  anonymizedCompany?: string | null
  status?: ProjectStatus
  category?: ProjectCategory | null
  achievements?: string[]
  challenges?: string[]
  clients?: string[]
  team?: string[]
  subProjects?: SubProject[]
  teamSize?: number | null
  durationMonths?: number | null
  usersCount?: number | null
  budgetRange?: string | null
  links?: ProjectLinks
  visibility?: ProfileVisibility
  technologies?: string[]
  experienceIds?: string[]
}

export interface IProjectService {
  list(): Promise<Project[]>
  create(data: CreateProjectData): Promise<Project>
  update(id: string, data: UpdateProjectData): Promise<Project>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Project[]>
}
