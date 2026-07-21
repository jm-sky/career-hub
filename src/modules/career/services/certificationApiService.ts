import { apiClient } from '@/shared/services/apiClient'
import type { Certification, CreateCertificationData, ICertificationService, UpdateCertificationData } from '@/modules/career/types/certification.type'

class CertificationApiService implements ICertificationService {
  async list(): Promise<Certification[]> {
    const response = await apiClient.get<Certification[]>('/career/certifications')
    return response.data
  }

  async create(data: CreateCertificationData): Promise<Certification> {
    const response = await apiClient.post<Certification>('/career/certifications', data)
    return response.data
  }

  async update(id: string, data: UpdateCertificationData): Promise<Certification> {
    const response = await apiClient.put<Certification>(`/career/certifications/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/certifications/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Certification[]> {
    const response = await apiClient.put<Certification[]>('/career/certifications/reorder', { orderedIds })
    return response.data
  }
}

export const certificationApiService = new CertificationApiService()
