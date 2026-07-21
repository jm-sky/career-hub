import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { projectApiService } from '@/modules/career/services/projectApiService'
import { profileMutationRetryFunction, profileRetryFunction, projectQueryKeys } from '@/modules/career/utils/queryUtils'
import type { CreateProjectData, IProjectService, Project, UpdateProjectData } from '@/modules/career/types/project.type'

export function useProjectsQuery(service?: IProjectService) {
  return useQuery({
    queryKey: projectQueryKeys.all,
    queryFn: () => (service ?? projectApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateProject(service?: IProjectService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateProjectData) => (service ?? projectApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: projectQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateProject(service?: IProjectService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateProjectData }) => (service ?? projectApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: projectQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteProject(service?: IProjectService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? projectApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: projectQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderProjects(service?: IProjectService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? projectApiService).reorder(orderedIds),
    onSuccess: (updated: Project[]) => queryClient.setQueryData(projectQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useProjects(service?: IProjectService) {
  const projectsQuery = useProjectsQuery(service)
  const createMutation = useCreateProject(service)
  const updateMutation = useUpdateProject(service)
  const deleteMutation = useDeleteProject(service)
  const reorderMutation = useReorderProjects(service)

  return {
    projectsQuery,
    projects: projectsQuery.data,
    isLoading: projectsQuery.isLoading,
    isError: projectsQuery.isError,
    error: projectsQuery.error,
    createProject: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateProject: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteProject: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderProjects: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
