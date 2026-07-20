import { apiClient } from '@/shared/services/apiClient'
import type { IProfileService, Profile, ProfileDraftData, PublicProfile, UpdateProfileData } from '@/modules/career/types/profile.type'

class ProfileApiService implements IProfileService {
  async getMyProfile(): Promise<Profile> {
    const response = await apiClient.get<Profile>('/career/profile')
    return response.data
  }

  async updateMyProfile(data: UpdateProfileData): Promise<Profile> {
    const response = await apiClient.put<Profile>('/career/profile', data)
    return response.data
  }

  async saveDraft(draft: ProfileDraftData): Promise<Profile> {
    const response = await apiClient.post<Profile>('/career/profile/draft', draft)
    return response.data
  }

  async getPublicProfile(slug: string): Promise<PublicProfile> {
    const response = await apiClient.get<PublicProfile>(`/career/profile/${slug}`)
    return response.data
  }
}

export const profileApiService = new ProfileApiService()
