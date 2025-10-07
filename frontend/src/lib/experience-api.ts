// Experience API functions using axios client

import apiClient from './api-client';
import {
  Experience,
  ExperienceCreate,
  ExperienceUpdate,
  ExperienceSummary,
} from '@/types/experience';

export const experienceAPI = {
  /**
   * Create a new experience for a profile
   */
  async createExperience(profileId: string, experienceData: ExperienceCreate): Promise<Experience> {
    const { data } = await apiClient.post<Experience>('/experiences/', experienceData, {
      params: { profile_id: profileId },
    });
    return data;
  },

  /**
   * Get experience by ID
   */
  async getExperienceById(experienceId: string): Promise<Experience> {
    const { data } = await apiClient.get<Experience>(`/experiences/${experienceId}`);
    return data;
  },

  /**
   * Update experience
   */
  async updateExperience(experienceId: string, experienceData: ExperienceUpdate): Promise<Experience> {
    const { data } = await apiClient.put<Experience>(`/experiences/${experienceId}`, experienceData);
    return data;
  },

  /**
   * Delete experience
   */
  async deleteExperience(experienceId: string): Promise<void> {
    await apiClient.delete(`/experiences/${experienceId}`);
  },

  /**
   * Get all experiences for a profile
   */
  async getProfileExperiences(profileId: string): Promise<ExperienceSummary[]> {
    const { data } = await apiClient.get<ExperienceSummary[]>(`/experiences/profile/${profileId}`);
    return data;
  },

  /**
   * Reorder experiences for a profile
   */
  async reorderExperiences(profileId: string, experienceIds: string[]): Promise<ExperienceSummary[]> {
    const { data } = await apiClient.post<ExperienceSummary[]>(
      `/experiences/profile/${profileId}/reorder`,
      { experienceIds }
    );
    return data;
  },

  /**
   * Add responsibility to experience
   */
  async addResponsibility(experienceId: string, responsibility: string): Promise<Experience> {
    const { data } = await apiClient.post<Experience>(
      `/experiences/${experienceId}/responsibilities`,
      null,
      { params: { responsibility } }
    );
    return data;
  },

  /**
   * Remove responsibility from experience
   */
  async removeResponsibility(experienceId: string, responsibility: string): Promise<Experience> {
    const { data } = await apiClient.delete<Experience>(
      `/experiences/${experienceId}/responsibilities`,
      { params: { responsibility } }
    );
    return data;
  },

  /**
   * Add technology to experience
   */
  async addTechnology(experienceId: string, technology: string): Promise<Experience> {
    const { data } = await apiClient.post<Experience>(
      `/experiences/${experienceId}/technologies`,
      null,
      { params: { technology } }
    );
    return data;
  },

  /**
   * Remove technology from experience
   */
  async removeTechnology(experienceId: string, technology: string): Promise<Experience> {
    const { data } = await apiClient.delete<Experience>(
      `/experiences/${experienceId}/technologies`,
      { params: { technology } }
    );
    return data;
  },
};
