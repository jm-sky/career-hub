import { apiClient } from '@/shared/services/apiClient'
import type { CareerOverview, ICareerOverviewService } from '@/modules/career/types/careerOverview.type'

class CareerOverviewApiService implements ICareerOverviewService {
  async getOverview(): Promise<CareerOverview> {
    const response = await apiClient.get<CareerOverview>('/career/overview')
    return response.data
  }
}

export const careerOverviewApiService = new CareerOverviewApiService()
