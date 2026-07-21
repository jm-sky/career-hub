import { apiClient } from '@/shared/services/apiClient'
import type { CreateLanguageData, ILanguageService, Language, UpdateLanguageData } from '@/modules/career/types/language.type'

class LanguageApiService implements ILanguageService {
  async list(): Promise<Language[]> {
    const response = await apiClient.get<Language[]>('/career/languages')
    return response.data
  }

  async create(data: CreateLanguageData): Promise<Language> {
    const response = await apiClient.post<Language>('/career/languages', data)
    return response.data
  }

  async update(id: string, data: UpdateLanguageData): Promise<Language> {
    const response = await apiClient.put<Language>(`/career/languages/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/languages/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Language[]> {
    const response = await apiClient.put<Language[]>('/career/languages/reorder', { orderedIds })
    return response.data
  }
}

export const languageApiService = new LanguageApiService()
