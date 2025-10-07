// TanStack Query hooks for experience management

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { experienceAPI } from '@/lib/experience-api';
import {
  Experience,
  ExperienceCreate,
  ExperienceUpdate,
  ExperienceSummary,
} from '@/types/experience';
import { profileKeys } from './use-profile';

// Query keys
export const experienceKeys = {
  all: ['experiences'] as const,
  lists: () => [...experienceKeys.all, 'list'] as const,
  list: (profileId: string) => [...experienceKeys.lists(), profileId] as const,
  details: () => [...experienceKeys.all, 'detail'] as const,
  detail: (id: string) => [...experienceKeys.details(), id] as const,
};

/**
 * Hook to get experience by ID
 */
export const useExperience = (experienceId: string) => {
  return useQuery({
    queryKey: experienceKeys.detail(experienceId),
    queryFn: () => experienceAPI.getExperienceById(experienceId),
    enabled: !!experienceId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to get all experiences for a profile
 */
export const useProfileExperiences = (profileId: string) => {
  return useQuery({
    queryKey: experienceKeys.list(profileId),
    queryFn: () => experienceAPI.getProfileExperiences(profileId),
    enabled: !!profileId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook for creating an experience
 */
export const useCreateExperience = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ profileId, experienceData }: { profileId: string; experienceData: ExperienceCreate }) =>
      experienceAPI.createExperience(profileId, experienceData),
    onSuccess: (data, variables) => {
      // Invalidate experiences list for the profile
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(variables.profileId) });
      
      // Invalidate profile data to update completeness score
      queryClient.invalidateQueries({ queryKey: profileKeys.detail(variables.profileId) });
      queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
    },
    onError: (error) => {
      console.error('Experience creation failed:', error);
    },
  });
};

/**
 * Hook for updating an experience
 */
export const useUpdateExperience = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ experienceId, experienceData }: { experienceId: string; experienceData: ExperienceUpdate }) =>
      experienceAPI.updateExperience(experienceId, experienceData),
    onSuccess: (data, variables) => {
      // Update specific experience cache
      queryClient.setQueryData(experienceKeys.detail(variables.experienceId), data);
      
      // Invalidate experiences list for the profile
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(data.profileId) });
      
      // Invalidate profile data to update completeness score
      queryClient.invalidateQueries({ queryKey: profileKeys.detail(data.profileId) });
      queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
    },
    onError: (error) => {
      console.error('Experience update failed:', error);
    },
  });
};

/**
 * Hook for deleting an experience
 */
export const useDeleteExperience = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (experienceId: string) => experienceAPI.deleteExperience(experienceId),
    onMutate: async (experienceId) => {
      // Get the experience data before deletion for cleanup
      const experience = queryClient.getQueryData<Experience>(experienceKeys.detail(experienceId));
      return { experience };
    },
    onSuccess: (_, experienceId, context) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: experienceKeys.detail(experienceId) });
      
      if (context?.experience) {
        // Invalidate experiences list for the profile
        queryClient.invalidateQueries({ queryKey: experienceKeys.list(context.experience.profileId) });
        
        // Invalidate profile data to update completeness score
        queryClient.invalidateQueries({ queryKey: profileKeys.detail(context.experience.profileId) });
        queryClient.invalidateQueries({ queryKey: profileKeys.myProfile() });
      }
    },
    onError: (error) => {
      console.error('Experience deletion failed:', error);
    },
  });
};

/**
 * Hook for reordering experiences
 */
export const useReorderExperiences = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ profileId, experienceIds }: { profileId: string; experienceIds: string[] }) =>
      experienceAPI.reorderExperiences(profileId, experienceIds),
    onSuccess: (data, variables) => {
      // Update experiences list cache with new order
      queryClient.setQueryData(experienceKeys.list(variables.profileId), data);
    },
    onError: (error) => {
      console.error('Experience reordering failed:', error);
    },
  });
};

/**
 * Hook for adding a responsibility to an experience
 */
export const useAddResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ experienceId, responsibility }: { experienceId: string; responsibility: string }) =>
      experienceAPI.addResponsibility(experienceId, responsibility),
    onSuccess: (data, variables) => {
      // Update experience cache
      queryClient.setQueryData(experienceKeys.detail(variables.experienceId), data);
      
      // Invalidate experiences list
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Adding responsibility failed:', error);
    },
  });
};

/**
 * Hook for removing a responsibility from an experience
 */
export const useRemoveResponsibility = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ experienceId, responsibility }: { experienceId: string; responsibility: string }) =>
      experienceAPI.removeResponsibility(experienceId, responsibility),
    onSuccess: (data, variables) => {
      // Update experience cache
      queryClient.setQueryData(experienceKeys.detail(variables.experienceId), data);
      
      // Invalidate experiences list
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Removing responsibility failed:', error);
    },
  });
};

/**
 * Hook for adding a technology to an experience
 */
export const useAddTechnology = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ experienceId, technology }: { experienceId: string; technology: string }) =>
      experienceAPI.addTechnology(experienceId, technology),
    onSuccess: (data, variables) => {
      // Update experience cache
      queryClient.setQueryData(experienceKeys.detail(variables.experienceId), data);
      
      // Invalidate experiences list
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Adding technology failed:', error);
    },
  });
};

/**
 * Hook for removing a technology from an experience
 */
export const useRemoveTechnology = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ experienceId, technology }: { experienceId: string; technology: string }) =>
      experienceAPI.removeTechnology(experienceId, technology),
    onSuccess: (data, variables) => {
      // Update experience cache
      queryClient.setQueryData(experienceKeys.detail(variables.experienceId), data);
      
      // Invalidate experiences list
      queryClient.invalidateQueries({ queryKey: experienceKeys.list(data.profileId) });
    },
    onError: (error) => {
      console.error('Removing technology failed:', error);
    },
  });
};
