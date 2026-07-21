import { apiClient } from '@/shared/services/apiClient'
import type { CreateProjectData, IProjectService, Project, UpdateProjectData } from '@/modules/career/types/project.type'

class ProjectApiService implements IProjectService {
  async list(): Promise<Project[]> {
    const response = await apiClient.get<Project[]>('/career/projects')
    return response.data
  }

  async create(data: CreateProjectData): Promise<Project> {
    const response = await apiClient.post<Project>('/career/projects', data)
    return response.data
  }

  async update(id: string, data: UpdateProjectData): Promise<Project> {
    const response = await apiClient.put<Project>(`/career/projects/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/career/projects/${id}`)
  }

  async reorder(orderedIds: string[]): Promise<Project[]> {
    const response = await apiClient.put<Project[]>('/career/projects/reorder', { orderedIds })
    return response.data
  }
}

export const projectApiService = new ProjectApiService()
