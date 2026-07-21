import type { RouteRecordRaw } from 'vue-router'

export const CareerRoutePaths = {
  profileEdit: import.meta.env.VITE_PROFILE_EDIT_PATH ?? '/profile',
  experiences: '/experiences',
  skills: '/skills',
  projects: '/projects',
  publicProfile: '/p/:slug',
} as const

export const CareerRouteNames = {
  profileEdit: 'career-profile-edit',
  experiences: 'career-experiences',
  skills: 'career-skills',
  projects: 'career-projects',
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
    path: CareerRoutePaths.experiences,
    name: CareerRouteNames.experiences,
    component: () => import('@/modules/career/pages/ExperiencesPage.vue'),
    meta: { layout: 'authenticated', title: 'career.experiences.page.title' },
  },
  {
    path: CareerRoutePaths.skills,
    name: CareerRouteNames.skills,
    component: () => import('@/modules/career/pages/SkillsPage.vue'),
    meta: { layout: 'authenticated', title: 'career.skills.page.title' },
  },
  {
    path: CareerRoutePaths.projects,
    name: CareerRouteNames.projects,
    component: () => import('@/modules/career/pages/ProjectsPage.vue'),
    meta: { layout: 'authenticated', title: 'career.projects.page.title' },
  },
  {
    path: CareerRoutePaths.publicProfile,
    name: CareerRouteNames.publicProfile,
    component: () => import('@/modules/career/pages/PublicProfilePage.vue'),
    meta: { layout: 'public', title: 'career.publicProfile.page.title' },
  },
]
