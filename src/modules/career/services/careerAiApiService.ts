import { apiClient } from '@/shared/services/apiClient'
import type {
  AnalyzeProfileResult,
  ICareerAiService,
  OptimizeDescriptionData,
  OptimizeDescriptionResult,
  SuggestResponsibilitiesData,
  SuggestResponsibilitiesResult,
} from '@/modules/career/types/ai.type'

class CareerAiApiService implements ICareerAiService {
  async optimizeDescription(data: OptimizeDescriptionData): Promise<OptimizeDescriptionResult> {
    const response = await apiClient.post<OptimizeDescriptionResult>('/career/ai/optimize-description', data)
    return response.data
  }

  async suggestResponsibilities(data: SuggestResponsibilitiesData): Promise<SuggestResponsibilitiesResult> {
    const response = await apiClient.post<SuggestResponsibilitiesResult>('/career/ai/suggest-responsibilities', data)
    return response.data
  }

  async analyzeProfile(targetRole: string): Promise<AnalyzeProfileResult> {
    const response = await apiClient.post<AnalyzeProfileResult>('/career/ai/analyze-profile', { targetRole })
    return response.data
  }
}

export const careerAiApiService = new CareerAiApiService()
