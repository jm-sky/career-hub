import { useQuery } from '@tanstack/vue-query'
import { computed, unref } from 'vue'
import { technologyApiService } from '@/modules/career/services/technologyApiService'
import { profileRetryFunction, technologyQueryKeys } from '@/modules/career/utils/queryUtils'
import type { MaybeRef } from 'vue'
import type { ITechnologyService } from '@/modules/career/types/technology.type'

/** Reactive technology search — refetches whenever `query`'s value changes. */
export function useTechnologySearch(query: MaybeRef<string | undefined>, service?: ITechnologyService) {
  return useQuery({
    queryKey: computed(() => technologyQueryKeys.search(unref(query))),
    queryFn: () => (service ?? technologyApiService).search(unref(query)),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}
