import { apiClient } from '@/shared/services/apiClient'
import type { CreateEducationData, Education, IEducationService, UpdateEducationData } from '@/modules/career/types/education.type'

class EducationApiService implements IEducationService {
  async list(): Promise<Education[]> {
    const response = await apiClient.get<Education[]>('/career/education')
    return response.data
  }

  async create(data: CreateEducationData): Promise<Education> {
    const response = await apiClient.post<Education>('/career/education', data)
    return response.data
  }

  async update(id: string, data: UpdateEducationData): Promise<Education> {
    const response = await apiClient.put<Education>(`/career/education/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/education/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Education[]> {
    const response = await apiClient.put<Education[]>('/career/education/reorder', { orderedIds })
    return response.data
  }
}

export const educationApiService = new EducationApiService()
