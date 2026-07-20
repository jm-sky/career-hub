import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export interface IUseSearchPaginationUrlOptions {
  defaultPageSize?: number
  searchParam?: string
  pageParam?: string
  pageSizeParam?: string
}

/**
 * Syncs search text, current page, and page size with the route's query params
 * (two-way: reads initial values from the URL, writes changes back via router.replace).
 */
export function useSearchPaginationUrl(options: IUseSearchPaginationUrlOptions = {}) {
  const {
    defaultPageSize = 20,
    searchParam = 'search',
    pageParam = 'page',
    pageSizeParam = 'pageSize',
  } = options

  const route = useRoute()
  const router = useRouter()

  const updateQuery = (patch: Record<string, string | undefined>): void => {
    const query = { ...route.query }
    for (const [key, value] of Object.entries(patch)) {
      if (value === undefined || value === '') {
        delete query[key]
      } else {
        query[key] = value
      }
    }
    router.replace({ query })
  }

  const search = computed<string>({
    get: () => (typeof route.query[searchParam] === 'string' ? route.query[searchParam] as string : ''),
    set: (value: string) => updateQuery({ [searchParam]: value || undefined, [pageParam]: undefined }),
  })

  const page = computed<number>({
    get: () => {
      const raw = route.query[pageParam]
      const parsed = typeof raw === 'string' ? Number.parseInt(raw, 10) : NaN
      return Number.isFinite(parsed) && parsed > 0 ? parsed : 1
    },
    set: (value: number) => updateQuery({ [pageParam]: value > 1 ? String(value) : undefined }),
  })

  const pageSize = computed<number>({
    get: () => {
      const raw = route.query[pageSizeParam]
      const parsed = typeof raw === 'string' ? Number.parseInt(raw, 10) : NaN
      return Number.isFinite(parsed) && parsed > 0 ? parsed : defaultPageSize
    },
    set: (value: number) => updateQuery({ [pageSizeParam]: value !== defaultPageSize ? String(value) : undefined }),
  })

  return {
    search,
    page,
    pageSize,
  }
}
