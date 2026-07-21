import { apiClient } from '@/shared/services/apiClient'
import type { ITechnologyService, Technology } from '@/modules/career/types/technology.type'

class TechnologyApiService implements ITechnologyService {
  async search(query?: string, limit = 20): Promise<Technology[]> {
    const response = await apiClient.get<Technology[]>('/career/technologies', { params: { q: query, limit } })
    return response.data
  }
}

export const technologyApiService = new TechnologyApiService()
