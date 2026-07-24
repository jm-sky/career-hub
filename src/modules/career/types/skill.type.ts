import type { Technology } from '@/modules/career/types/technology.type'

export interface Skill {
  id: string
  profileId: string
  technology: Technology
  level: number
  yearsOfExperience: number | null
  startedUsingYear: number | null
  isPrimary: boolean
  createdAt: string
  updatedAt: string
}

export interface CreateSkillData {
  technologyName: string
  level: number
  yearsOfExperience?: number | null
  startedUsingYear?: number | null
  isPrimary?: boolean
}

export interface UpdateSkillData {
  level?: number
  yearsOfExperience?: number | null
  startedUsingYear?: number | null
  isPrimary?: boolean
}

export interface ISkillService {
  list(): Promise<Skill[]>
  create(data: CreateSkillData): Promise<Skill>
  bulkUpsert(skills: CreateSkillData[]): Promise<Skill[]>
  update(id: string, data: UpdateSkillData): Promise<Skill>
  delete(id: string): Promise<void>
  suggestions(role: string, seniorityLevel?: string): Promise<string[]>
}
