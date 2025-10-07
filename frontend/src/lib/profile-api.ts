// Profile API functions using axios client

import apiClient from './api-client';
import {
  Profile,
  ProfileCreate,
  ProfileUpdate,
  ProfileSummary,
  ProfilePublic,
} from '@/types/profile';

export const profileAPI = {
  /**
   * Create a new profile for the current user
   */
  async createProfile(profileData: ProfileCreate): Promise<Profile> {
    const { data } = await apiClient.post<Profile>('/profiles/', profileData);
    return data;
  },

  /**
   * Get current user's profile
   */
  async getMyProfile(): Promise<Profile> {
    const { data } = await apiClient.get<Profile>('/profiles/me');
    return data;
  },

  /**
   * Get profile by ID
   */
  async getProfileById(profileId: string): Promise<Profile> {
    const { data } = await apiClient.get<Profile>(`/profiles/${profileId}`);
    return data;
  },

  /**
   * Update profile
   */
  async updateProfile(profileId: string, profileData: ProfileUpdate): Promise<Profile> {
    const { data } = await apiClient.put<Profile>(`/profiles/${profileId}`, profileData);
    return data;
  },

  /**
   * Delete profile
   */
  async deleteProfile(profileId: string): Promise<void> {
    await apiClient.delete(`/profiles/${profileId}`);
  },

  /**
   * Get public profiles
   */
  async getPublicProfiles(limit = 20, offset = 0): Promise<ProfileSummary[]> {
    const { data } = await apiClient.get<ProfileSummary[]>('/profiles/', {
      params: { limit, offset },
    });
    return data;
  },

  /**
   * Search public profiles
   */
  async searchProfiles(query: string, limit = 20, offset = 0): Promise<ProfileSummary[]> {
    const { data } = await apiClient.get<ProfileSummary[]>('/profiles/search/', {
      params: { q: query, limit, offset },
    });
    return data;
  },

  /**
   * Get public profile by slug
   */
  async getProfileBySlug(slug: string): Promise<ProfilePublic> {
    const { data } = await apiClient.get<ProfilePublic>(`/profiles/slug/${slug}`);
    return data;
  },

  /**
   * Update profile completeness score
   */
  async updateCompletenessScore(profileId: string): Promise<{ completenessScore: number }> {
    const { data } = await apiClient.post<{ completenessScore: number }>(`/profiles/${profileId}/completeness`);
    return data;
  },

  /**
   * Check if slug is available
   */
  async checkSlugAvailability(slug: string, profileId?: string): Promise<{ available: boolean }> {
    const { data } = await apiClient.get<{ available: boolean }>(`/profiles/slug-available/${slug}`, {
      params: profileId ? { profileId } : {},
    });
    return data;
  },
};
