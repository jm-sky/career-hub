import { apiClient } from '@/shared/services/apiClient'
import type { CreateCvVersionData, CvVersion, GenerateCvVersionResult, ICvVersionService, UpdateCvVersionData } from '@/modules/career/types/cvVersion.type'

class CvVersionApiService implements ICvVersionService {
  async list(): Promise<CvVersion[]> {
    const response = await apiClient.get<CvVersion[]>('/career/cv-versions')
    return response.data
  }

  async create(data: CreateCvVersionData): Promise<CvVersion> {
    const response = await apiClient.post<CvVersion>('/career/cv-versions', data)
    return response.data
  }

  async update(id: string, data: UpdateCvVersionData): Promise<CvVersion> {
    const response = await apiClient.put<CvVersion>(`/career/cv-versions/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/cv-versions/${id}`)
  }

  async generate(id: string): Promise<GenerateCvVersionResult> {
    const response = await apiClient.post<GenerateCvVersionResult>(`/career/cv-versions/${id}/generate`)
    return response.data
  }

  async getDownloadUrl(id: string): Promise<string> {
    const response = await apiClient.get<{ pdfUrl: string }>(`/career/cv-versions/${id}/download`)
    return response.data.pdfUrl
  }
}

export const cvVersionApiService = new CvVersionApiService()
