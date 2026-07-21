import { apiClient } from '@/shared/services/apiClient'
import type { CreateSkillData, ISkillService, Skill, UpdateSkillData } from '@/modules/career/types/skill.type'

class SkillApiService implements ISkillService {
  async list(): Promise<Skill[]> {
    const response = await apiClient.get<Skill[]>('/career/skills')
    return response.data
  }

  async create(data: CreateSkillData): Promise<Skill> {
    const response = await apiClient.post<Skill>('/career/skills', data)
    return response.data
  }

  async bulkUpsert(skills: CreateSkillData[]): Promise<Skill[]> {
    const response = await apiClient.post<Skill[]>('/career/skills/bulk', { skills })
    return response.data
  }

  async update(id: string, data: UpdateSkillData): Promise<Skill> {
    const response = await apiClient.put<Skill>(`/career/skills/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/skills/${id}`)
  }

  async suggestions(role?: string): Promise<string[]> {
    const response = await apiClient.get<string[]>('/career/skills/suggestions', { params: { role } })
    return response.data
  }
}

export const skillApiService = new SkillApiService()
