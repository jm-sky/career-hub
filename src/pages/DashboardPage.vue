<script setup lang="ts">
import {
  ArrowRight,
  Award,
  Briefcase,
  ExternalLink,
  FilePlus2,
  FileStack,
  FolderKanban,
  GraduationCap,
  Languages,
  Lightbulb,
  LogIn,
  Sparkles,
  Star,
  UserCircle2,
  UserPen,
  UserPlus,
} from 'lucide-vue-next'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ButtonLink from '@/components/ui/button-link/ButtonLink.vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import { useAuth } from '@/modules/auth/composables/useAuth'
import { AuthRoutePaths } from '@/modules/auth/config/routes'
import UpgradePromptBanner from '@/modules/billing/components/UpgradePromptBanner.vue'
import { useCareerOverview } from '@/modules/career/composables/useCareerOverview'
import { CareerRoutePaths, publicProfilePath } from '@/modules/career/routes'
import { config } from '@/shared/config/config'
import type { Component } from 'vue'
import type { CareerSectionCounts } from '@/modules/career/types/careerOverview.type'

const { t } = useI18n()
const { isAuthenticated } = useAuth()

const showOverview = computed<boolean>(() => isAuthenticated.value && config.backend.enabled)

const { overview, isLoading, isError } = useCareerOverview({ enabled: showOverview })

interface SectionCard {
  key: keyof CareerSectionCounts
  icon: Component
  to: string
}

const sectionCards: SectionCard[] = [
  { key: 'experiences', icon: Briefcase, to: CareerRoutePaths.experiences },
  { key: 'projects', icon: FolderKanban, to: CareerRoutePaths.projects },
  { key: 'skills', icon: Sparkles, to: CareerRoutePaths.skills },
  { key: 'education', icon: GraduationCap, to: CareerRoutePaths.education },
  { key: 'certifications', icon: Award, to: CareerRoutePaths.certifications },
  { key: 'achievements', icon: Star, to: CareerRoutePaths.achievements },
  { key: 'languages', icon: Languages, to: CareerRoutePaths.languages },
  { key: 'cvVersions', icon: FileStack, to: CareerRoutePaths.cvVersions },
]

const suggestionRoutes: Record<string, string> = {
  addHeadline: CareerRoutePaths.profileEdit,
  addSummary: CareerRoutePaths.profileEdit,
  addPhoto: CareerRoutePaths.profileEdit,
  makePublic: CareerRoutePaths.profileEdit,
  addExperience: CareerRoutePaths.experiences,
  addSkills: CareerRoutePaths.skills,
  addProject: CareerRoutePaths.projects,
  addEducation: CareerRoutePaths.education,
  addLanguage: CareerRoutePaths.languages,
  createCv: CareerRoutePaths.cvVersions,
}

const publicProfileUrl = computed<string | null>(() => {
  if (!overview.value || overview.value.visibility !== 'PUBLIC') return null
  return publicProfilePath(overview.value.slug)
})
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-8">
      <!-- Upgrade Prompt Banner (only for authenticated FREE users) -->
      <UpgradePromptBanner v-if="isAuthenticated && config.backend.enabled" />

      <!-- Career overview (authenticated) -->
      <template v-if="showOverview">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ t('career.overview.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ overview?.headline || t('career.overview.subtitle') }}
          </p>
        </div>

        <div v-if="isLoading" class="space-y-4">
          <div class="h-32 bg-muted rounded-xl animate-pulse" />
          <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            <div
              v-for="index in 8"
              :key="index"
              class="h-24 bg-muted rounded-xl animate-pulse"
            />
          </div>
        </div>

        <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
          {{ t('career.overview.error') }}
        </div>

        <template v-else-if="overview">
          <!-- Profile strength + suggestions -->
          <div class="grid gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle class="flex items-center justify-between text-base">
                  {{ t('career.overview.completeness') }}
                  <span class="text-2xl font-bold text-primary">{{ overview.completenessScore }}%</span>
                </CardTitle>
              </CardHeader>
              <CardContent class="space-y-3">
                <Progress :model-value="overview.completenessScore" />
                <p class="text-sm text-muted-foreground">
                  {{ t('career.overview.completenessHint') }}
                </p>
              </CardContent>
            </Card>

            <Card v-if="overview.suggestions.length">
              <CardHeader>
                <CardTitle class="flex items-center gap-2 text-base">
                  <Lightbulb class="size-4 text-warm" />
                  {{ t('career.overview.suggestions.title') }}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul class="space-y-2">
                  <li v-for="suggestion in overview.suggestions" :key="suggestion">
                    <RouterLink
                      :to="suggestionRoutes[suggestion] ?? CareerRoutePaths.profileEdit"
                      class="group flex items-center gap-2 text-sm text-foreground/80 hover:text-primary transition-colors"
                    >
                      <ArrowRight class="size-3.5 shrink-0 transition-transform group-hover:translate-x-0.5" />
                      {{ t(`career.overview.suggestions.${suggestion}`) }}
                    </RouterLink>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>

          <!-- Section counts -->
          <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            <RouterLink
              v-for="section in sectionCards"
              :key="section.key"
              :to="section.to"
              class="block rounded-xl focus-visible:outline-2 focus-visible:outline-ring"
            >
              <Card class="h-full gap-2 py-4">
                <CardContent class="flex items-center gap-3 px-4">
                  <div class="rounded-lg bg-primary/10 p-2.5">
                    <component :is="section.icon" class="size-5 text-primary" />
                  </div>
                  <div class="min-w-0">
                    <div class="text-2xl font-bold leading-tight">
                      {{ overview.counts[section.key] }}
                    </div>
                    <div class="truncate text-xs text-muted-foreground">
                      {{ t(`career.overview.sections.${section.key}`) }}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </RouterLink>
          </div>

          <!-- Quick actions -->
          <div class="flex flex-wrap gap-3">
            <ButtonLink variant="default" :to="CareerRoutePaths.profileEdit">
              <UserPen class="size-4" />
              {{ t('career.overview.quickActions.editProfile') }}
            </ButtonLink>
            <ButtonLink variant="outline" :to="CareerRoutePaths.experiences">
              <Briefcase class="size-4" />
              {{ t('career.overview.quickActions.addExperience') }}
            </ButtonLink>
            <ButtonLink variant="outline" :to="CareerRoutePaths.cvVersions">
              <FilePlus2 class="size-4" />
              {{ t('career.overview.quickActions.newCv') }}
            </ButtonLink>
            <ButtonLink
              v-if="publicProfileUrl"
              variant="outline"
              :to="publicProfileUrl"
            >
              <ExternalLink class="size-4" />
              {{ t('career.overview.quickActions.viewPublic') }}
            </ButtonLink>
          </div>
        </template>
      </template>

      <!-- Guest hero -->
      <template v-else>
        <div class="text-center space-y-4">
          <div class="flex justify-center">
            <div class="rounded-full bg-primary/10 p-6">
              <UserCircle2 class="size-16 text-primary" />
            </div>
          </div>
          <h1 class="text-4xl font-bold">
            {{ t('dashboard.title', 'CareerHub') }}
          </h1>
          <p class="text-muted-foreground text-lg max-w-2xl mx-auto">
            {{ t('dashboard.subtitle', 'Your professional profile and CV builder is coming soon.') }}
          </p>
        </div>

        <div v-if="!isAuthenticated && config.backend.enabled" class="flex flex-col items-center gap-4">
          <div class="flex flex-col sm:flex-row gap-4 w-full max-w-md">
            <ButtonLink
              size="lg"
              variant="outline"
              class="flex-1"
              :to="AuthRoutePaths.login"
            >
              <LogIn class="size-5" />
              {{ t('auth.login', 'Log In') }}
            </ButtonLink>
            <ButtonLink
              size="lg"
              variant="outline"
              class="flex-1"
              :to="AuthRoutePaths.register"
            >
              <UserPlus class="size-5" />
              {{ t('auth.register', 'Sign Up') }}
            </ButtonLink>
          </div>
        </div>
      </template>
    </div>
  </AuthenticatedLayout>
</template>
