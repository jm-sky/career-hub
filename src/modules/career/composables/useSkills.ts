import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { skillApiService } from '@/modules/career/services/skillApiService'
import { profileMutationRetryFunction, profileRetryFunction, skillQueryKeys } from '@/modules/career/utils/queryUtils'
import type { CreateSkillData, ISkillService, UpdateSkillData } from '@/modules/career/types/skill.type'

export function useSkillsQuery(service?: ISkillService) {
  return useQuery({
    queryKey: skillQueryKeys.all,
    queryFn: () => (service ?? skillApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateSkill(service?: ISkillService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateSkillData) => (service ?? skillApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: skillQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useBulkUpsertSkills(service?: ISkillService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (skills: CreateSkillData[]) => (service ?? skillApiService).bulkUpsert(skills),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: skillQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateSkill(service?: ISkillService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateSkillData }) => (service ?? skillApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: skillQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteSkill(service?: ISkillService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? skillApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: skillQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useSkillSuggestions(role?: string, service?: ISkillService) {
  return useQuery({
    queryKey: skillQueryKeys.suggestions(role),
    queryFn: () => (service ?? skillApiService).suggestions(role),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useSkills(service?: ISkillService) {
  const skillsQuery = useSkillsQuery(service)
  const createMutation = useCreateSkill(service)
  const bulkUpsertMutation = useBulkUpsertSkills(service)
  const updateMutation = useUpdateSkill(service)
  const deleteMutation = useDeleteSkill(service)

  return {
    skillsQuery,
    skills: skillsQuery.data,
    isLoading: skillsQuery.isLoading,
    isError: skillsQuery.isError,
    error: skillsQuery.error,
    createSkill: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    bulkUpsertSkills: bulkUpsertMutation.mutateAsync,
    isBulkUpserting: bulkUpsertMutation.isPending,
    updateSkill: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteSkill: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
  }
}
