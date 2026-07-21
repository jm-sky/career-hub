import { apiClient } from '@/shared/services/apiClient'
import type { CreateExperienceData, Experience, IExperienceService, UpdateExperienceData } from '@/modules/career/types/experience.type'

class ExperienceApiService implements IExperienceService {
  async list(): Promise<Experience[]> {
    const response = await apiClient.get<Experience[]>('/career/experiences')
    return response.data
  }

  async create(data: CreateExperienceData): Promise<Experience> {
    const response = await apiClient.post<Experience>('/career/experiences', data)
    return response.data
  }

  async update(id: string, data: UpdateExperienceData): Promise<Experience> {
    const response = await apiClient.put<Experience>(`/career/experiences/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/experiences/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Experience[]> {
    const response = await apiClient.put<Experience[]>('/career/experiences/reorder', { orderedIds })
    return response.data
  }
}

export const experienceApiService = new ExperienceApiService()
