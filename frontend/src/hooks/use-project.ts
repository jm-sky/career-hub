// TanStack Query hooks for project management

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { projectAPI } from '@/lib/project-api';
import { Project, ProjectCreate, ProjectUpdate } from '@/types/project';
import { profileKeys } from './use-profile';

// Query keys
export const projectKeys = {
  all: ['projects'] as const,
  lists: () => [...projectKeys.all, 'list'] as const,
  list: (profileId: string) => [...projectKeys.lists(), profileId] as const,
  details: () => [...projectKeys.all, 'detail'] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
};

/**
 * Hook to get project by ID
 */
export const useProject = (projectId: string) => {
  return useQuery({
    queryKey: projectKeys.detail(projectId),
    queryFn: () => projectAPI.getProjectById(projectId),
    enabled: !!projectId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to get all projects for a profile
 */
export const useProfileProjects = (profileId: string) => {
  return useQuery({
    queryKey: projectKeys.list(profileId),
    queryFn: () => projectAPI.getProfileProjects(profileId),
    enabled: !!profileId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook for creating a project
 */
export const useCreateProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ profileId, projectData }: { profileId: string; projectData: ProjectCreate }) =>
      projectAPI.createProject(profileId, projectData),
    onSuccess: (data, variables) => {
      // Invalidate projects list for the profile
      queryClient.invalidateQueries({ queryKey: projectKeys.list(variables.profileId) });
      
      // Invalidate profile data to update completeness score
      queryClient.invalidateQueries({ queryKey: profileKeys.detail(variables.profileId) });
      queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
    },
    onError: (error) => {
      console.error('Project creation failed:', error);
    },
  });
};

/**
 * Hook for updating a project
 */
export const useUpdateProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, projectData }: { projectId: string; projectData: ProjectUpdate }) =>
      projectAPI.updateProject(projectId, projectData),
    onSuccess: (data, variables) => {
      // Update specific project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list for the profile
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
      
      // Invalidate profile data to update completeness score
      queryClient.invalidateQueries({ queryKey: profileKeys.detail(data.profileId) });
      queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
    },
    onError: (error) => {
      console.error('Project update failed:', error);
    },
  });
};

/**
 * Hook for deleting a project
 */
export const useDeleteProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (projectId: string) => projectAPI.deleteProject(projectId),
    onMutate: async (projectId) => {
      // Get the project data before deletion for cleanup
      const project = queryClient.getQueryData<Project>(projectKeys.detail(projectId));
      return { project };
    },
    onSuccess: (_, projectId, context) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: projectKeys.detail(projectId) });
      
      if (context?.project) {
        // Invalidate projects list for the profile
        queryClient.invalidateQueries({ queryKey: projectKeys.list(context.project.profileId) });
        
        // Invalidate profile data to update completeness score
        queryClient.invalidateQueries({ queryKey: profileKeys.detail(context.project.profileId) });
        queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
      }
    },
    onError: (error) => {
      console.error('Project deletion failed:', error);
    },
  });
};

/**
 * Hook for reordering projects
 */
export const useReorderProjects = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ profileId, projectIds }: { profileId: string; projectIds: string[] }) =>
      projectAPI.reorderProjects(profileId, projectIds),
    onSuccess: (data, variables) => {
      // Update projects list cache with new order
      queryClient.setQueryData(projectKeys.list(variables.profileId), data);
    },
    onError: (error) => {
      console.error('Project reordering failed:', error);
    },
  });
};

/**
 * Hook for adding a technology to a project
 */
export const useAddTechnology = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, technology }: { projectId: string; technology: string }) =>
      projectAPI.addTechnology(projectId, technology),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Adding technology failed:', error);
    },
  });
};

/**
 * Hook for removing a technology from a project
 */
export const useRemoveTechnology = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, technology }: { projectId: string; technology: string }) =>
      projectAPI.removeTechnology(projectId, technology),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Removing technology failed:', error);
    },
  });
};

/**
 * Hook for adding an achievement to a project
 */
export const useAddAchievement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, achievement }: { projectId: string; achievement: string }) =>
      projectAPI.addAchievement(projectId, achievement),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Adding achievement failed:', error);
    },
  });
};

/**
 * Hook for removing an achievement from a project
 */
export const useRemoveAchievement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, achievement }: { projectId: string; achievement: string }) =>
      projectAPI.removeAchievement(projectId, achievement),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Removing achievement failed:', error);
    },
  });
};

/**
 * Hook for adding a challenge to a project
 */
export const useAddChallenge = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, challenge }: { projectId: string; challenge: string }) =>
      projectAPI.addChallenge(projectId, challenge),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Adding challenge failed:', error);
    },
  });
};

/**
 * Hook for removing a challenge from a project
 */
export const useRemoveChallenge = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, challenge }: { projectId: string; challenge: string }) =>
      projectAPI.removeChallenge(projectId, challenge),
    onSuccess: (data, variables) => {
      // Update project cache
      queryClient.setQueryData(projectKeys.detail(variables.projectId), data);
      
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: projectKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Removing challenge failed:', error);
    },
  });
};
