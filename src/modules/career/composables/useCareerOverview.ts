import { useQuery } from '@tanstack/vue-query'
import { careerOverviewApiService } from '@/modules/career/services/careerOverviewApiService'
import { careerOverviewQueryKeys, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { MaybeRefOrGetter } from 'vue'
import type { ICareerOverviewService } from '@/modules/career/types/careerOverview.type'

export function useCareerOverview(options?: { enabled?: MaybeRefOrGetter<boolean>, service?: ICareerOverviewService }) {
  const overviewQuery = useQuery({
    queryKey: careerOverviewQueryKeys.all,
    queryFn: () => (options?.service ?? careerOverviewApiService).getOverview(),
    staleTime: 30 * 1000,
    retry: profileRetryFunction,
    enabled: options?.enabled ?? true,
  })

  return {
    overviewQuery,
    overview: overviewQuery.data,
    isLoading: overviewQuery.isLoading,
    isError: overviewQuery.isError,
  }
}
