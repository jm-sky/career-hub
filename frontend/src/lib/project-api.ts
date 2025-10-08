// Project API client

import { apiClient } from './api-client';
import { Project, ProjectCreate, ProjectUpdate } from '@/types/project';

export const projectAPI = {
  /**
   * Get all projects for a profile
   */
  getProfileProjects: async (profileId: string): Promise<Project[]> => {
    const response = await apiClient.get(`/projects/profile/${profileId}`);
    return response.data;
  },

  /**
   * Get a specific project by ID
   */
  getProjectById: async (projectId: string): Promise<Project> => {
    const response = await apiClient.get(`/projects/${projectId}`);
    return response.data;
  },

  /**
   * Create a new project
   */
  createProject: async (profileId: string, projectData: ProjectCreate): Promise<Project> => {
    const response = await apiClient.post(`/projects/?profile_id=${profileId}`, projectData);
    return response.data;
  },

  /**
   * Update an existing project
   */
  updateProject: async (projectId: string, projectData: ProjectUpdate): Promise<Project> => {
    const response = await apiClient.patch(`/projects/${projectId}`, projectData);
    return response.data;
  },

  /**
   * Delete a project
   */
  deleteProject: async (projectId: string): Promise<void> => {
    await apiClient.delete(`/projects/${projectId}`);
  },

  /**
   * Reorder projects
   */
  reorderProjects: async (profileId: string, projectIds: string[]): Promise<Project[]> => {
    const response = await apiClient.post(`/projects/profile/${profileId}/reorder`, {
      project_ids: projectIds,
    });
    return response.data;
  },

  /**
   * Add a technology to a project
   */
  addTechnology: async (projectId: string, technology: string): Promise<Project> => {
    const response = await apiClient.post(`/projects/${projectId}/technologies`, {
      technology,
    });
    return response.data;
  },

  /**
   * Remove a technology from a project
   */
  removeTechnology: async (projectId: string, technology: string): Promise<Project> => {
    const response = await apiClient.delete(`/projects/${projectId}/technologies`, {
      data: { technology },
    });
    return response.data;
  },

  /**
   * Add an achievement to a project
   */
  addAchievement: async (projectId: string, achievement: string): Promise<Project> => {
    const response = await apiClient.post(`/projects/${projectId}/achievements`, {
      achievement,
    });
    return response.data;
  },

  /**
   * Remove an achievement from a project
   */
  removeAchievement: async (projectId: string, achievement: string): Promise<Project> => {
    const response = await apiClient.delete(`/projects/${projectId}/achievements`, {
      data: { achievement },
    });
    return response.data;
  },

  /**
   * Add a challenge to a project
   */
  addChallenge: async (projectId: string, challenge: string): Promise<Project> => {
    const response = await apiClient.post(`/projects/${projectId}/challenges`, {
      challenge,
    });
    return response.data;
  },

  /**
   * Remove a challenge from a project
   */
  removeChallenge: async (projectId: string, challenge: string): Promise<Project> => {
    const response = await apiClient.delete(`/projects/${projectId}/challenges`, {
      data: { challenge },
    });
    return response.data;
  },
};
