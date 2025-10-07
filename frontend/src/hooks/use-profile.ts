// TanStack Query hooks for profile management

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { profileAPI } from '@/lib/profile-api';
import {
  Profile,
  ProfileCreate,
  ProfileUpdate,
  ProfileSummary,
  ProfilePublic,
} from '@/types/profile';

// Query keys
export const profileKeys = {
  all: ['profiles'] as const,
  lists: () => [...profileKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...profileKeys.lists(), { filters }] as const,
  details: () => [...profileKeys.all, 'detail'] as const,
  detail: (id: string) => [...profileKeys.details(), id] as const,
  myProfile: () => [...profileKeys.all, 'my-profile'] as const,
  public: () => [...profileKeys.all, 'public'] as const,
  publicBySlug: (slug: string) => [...profileKeys.public(), slug] as const,
  search: (query: string) => [...profileKeys.all, 'search', query] as const,
};

/**
 * Hook to get current user's profile
 */
export const useMyProfile = () => {
  return useQuery({
    queryKey: profileKeys.myProfile(),
    queryFn: profileAPI.getMyProfile,
    retry: false, // Don't retry if user doesn't have a profile yet
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to get profile by ID
 */
export const useProfile = (profileId: string) => {
  return useQuery({
    queryKey: profileKeys.detail(profileId),
    queryFn: () => profileAPI.getProfileById(profileId),
    enabled: !!profileId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to get public profile by slug
 */
export const usePublicProfile = (slug: string) => {
  return useQuery({
    queryKey: profileKeys.publicBySlug(slug),
    queryFn: () => profileAPI.getProfileBySlug(slug),
    enabled: !!slug,
    staleTime: 10 * 60 * 1000, // 10 minutes for public profiles
  });
};

/**
 * Hook to get public profiles
 */
export const usePublicProfiles = (limit = 20, offset = 0) => {
  return useQuery({
    queryKey: profileKeys.list({ limit, offset }),
    queryFn: () => profileAPI.getPublicProfiles(limit, offset),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to search profiles
 */
export const useSearchProfiles = (query: string, limit = 20, offset = 0) => {
  return useQuery({
    queryKey: profileKeys.search(query),
    queryFn: () => profileAPI.searchProfiles(query, limit, offset),
    enabled: query.length >= 2, // Only search with at least 2 characters
    staleTime: 2 * 60 * 1000, // 2 minutes for search results
  });
};

/**
 * Hook for creating a profile
 */
export const useCreateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (profileData: ProfileCreate) => profileAPI.createProfile(profileData),
    onSuccess: (data) => {
      // Update my profile cache
      queryClient.setQueryData(profileKeys.myProfile(), data);
      
      // Invalidate profile lists
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
    },
    onError: (error) => {
      console.error('Profile creation failed:', error);
    },
  });
};

/**
 * Hook for updating a profile
 */
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ profileId, profileData }: { profileId: string; profileData: ProfileUpdate }) =>
      profileAPI.updateProfile(profileId, profileData),
    onSuccess: (data, variables) => {
      // Update specific profile cache
      queryClient.setQueryData(profileKeys.detail(variables.profileId), data);
      
      // Update my profile cache if it's the user's own profile
      const myProfile = queryClient.getQueryData<Profile>(profileKeys.myProfile());
      if (myProfile && myProfile.id === variables.profileId) {
        queryClient.setQueryData(profileKeys.myProfile(), data);
      }
      
      // Invalidate profile lists
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
    },
    onError: (error) => {
      console.error('Profile update failed:', error);
    },
  });
};

/**
 * Hook for deleting a profile
 */
export const useDeleteProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (profileId: string) => profileAPI.deleteProfile(profileId),
    onSuccess: (_, profileId) => {
      // Remove from all caches
      queryClient.removeQueries({ queryKey: profileKeys.detail(profileId) });
      queryClient.removeQueries({ queryKey: profileKeys.myProfile() });
      
      // Invalidate profile lists
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
    },
    onError: (error) => {
      console.error('Profile deletion failed:', error);
    },
  });
};

/**
 * Hook for updating profile completeness score
 */
export const useUpdateCompletenessScore = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (profileId: string) => profileAPI.updateCompletenessScore(profileId),
    onSuccess: (data, profileId) => {
      // Update profile caches with new completeness score
      const updateProfileData = (oldData: Profile | undefined) => {
        if (oldData) {
          return { ...oldData, completenessScore: data.completenessScore };
        }
        return oldData;
      };

      queryClient.setQueryData(profileKeys.detail(profileId), updateProfileData);
      
      const myProfile = queryClient.getQueryData<Profile>(profileKeys.myProfile());
      if (myProfile && myProfile.id === profileId) {
        queryClient.setQueryData(profileKeys.myProfile(), updateProfileData);
      }
    },
    onError: (error) => {
      console.error('Completeness score update failed:', error);
    },
  });
};

/**
 * Hook for checking slug availability
 */
export const useCheckSlugAvailability = () => {
  return useMutation({
    mutationFn: ({ slug, profileId }: { slug: string; profileId?: string }) =>
      profileAPI.checkSlugAvailability(slug, profileId),
  });
};
