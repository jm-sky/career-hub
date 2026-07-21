import { apiClient } from '@/shared/services/apiClient'
import type { Achievement, CreateAchievementData, IAchievementService, UpdateAchievementData } from '@/modules/career/types/achievement.type'

class AchievementApiService implements IAchievementService {
  async list(): Promise<Achievement[]> {
    const response = await apiClient.get<Achievement[]>('/career/achievements')
    return response.data
  }

  async create(data: CreateAchievementData): Promise<Achievement> {
    const response = await apiClient.post<Achievement>('/career/achievements', data)
    return response.data
  }

  async update(id: string, data: UpdateAchievementData): Promise<Achievement> {
    const response = await apiClient.put<Achievement>(`/career/achievements/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/achievements/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Achievement[]> {
    const response = await apiClient.put<Achievement[]>('/career/achievements/reorder', { orderedIds })
    return response.data
  }
}

export const achievementApiService = new AchievementApiService()
