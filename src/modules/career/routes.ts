import type { RouteRecordRaw } from 'vue-router'

export const CareerRoutePaths = {
  profileEdit: import.meta.env.VITE_PROFILE_EDIT_PATH ?? '/profile',
  publicProfile: '/p/:slug',
} as const

export const CareerRouteNames = {
  profileEdit: 'career-profile-edit',
  publicProfile: 'career-public-profile',
} as const

export function publicProfilePath(slug: string): string {
  return `/p/${slug}`
}

export const careerRoutes: RouteRecordRaw[] = [
  {
    path: CareerRoutePaths.profileEdit,
    name: CareerRouteNames.profileEdit,
    component: () => import('@/modules/career/pages/ProfileEditPage.vue'),
    meta: { layout: 'authenticated', title: 'career.profile.page.title' },
  },
  {
    path: CareerRoutePaths.publicProfile,
    name: CareerRouteNames.publicProfile,
    component: () => import('@/modules/career/pages/PublicProfilePage.vue'),
    meta: { layout: 'public', title: 'career.publicProfile.page.title' },
  },
]
