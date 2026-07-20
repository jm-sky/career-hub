import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { profileApiService } from '@/modules/career/services/profileApiService'
import { profileMutationRetryFunction, profileQueryKeys, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { IProfileService, Profile, ProfileDraftData, UpdateProfileData } from '@/modules/career/types/profile.type'

export function useProfileQuery(service?: IProfileService) {
  return useQuery({
    queryKey: profileQueryKeys.me(),
    queryFn: () => (service ?? profileApiService).getMyProfile(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useUpdateProfile(service?: IProfileService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: UpdateProfileData) => (service ?? profileApiService).updateMyProfile(data),
    onSuccess: (updated: Profile) => {
      queryClient.setQueryData(profileQueryKeys.me(), updated)
    },
    retry: profileMutationRetryFunction,
  })
}

export function useSaveProfileDraft(service?: IProfileService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (draft: ProfileDraftData) => (service ?? profileApiService).saveDraft(draft),
    onSuccess: (updated: Profile) => {
      queryClient.setQueryData(profileQueryKeys.me(), updated)
    },
    retry: profileMutationRetryFunction,
  })
}

export function useProfile(service?: IProfileService) {
  const queryClient = useQueryClient()

  const profileQuery = useProfileQuery(service)
  const updateMutation = useUpdateProfile(service)
  const draftMutation = useSaveProfileDraft(service)

  const refetchProfile = () => queryClient.invalidateQueries({ queryKey: profileQueryKeys.me() })

  return {
    profileQuery,
    profile: profileQuery.data,
    isLoading: profileQuery.isLoading,
    isError: profileQuery.isError,
    error: profileQuery.error,
    updateProfile: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    saveDraft: draftMutation.mutateAsync,
    isSavingDraft: draftMutation.isPending,
    refetchProfile,
  }
}

export function usePublicProfile(slug: string, service?: IProfileService) {
  return useQuery({
    queryKey: profileQueryKeys.public(slug),
    queryFn: () => (service ?? profileApiService).getPublicProfile(slug),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}
