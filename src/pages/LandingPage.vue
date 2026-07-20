<script setup lang="ts">
import { FileText } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import LandingLayout from '@/layouts/LandingLayout.vue'
import { useAuth } from '@/modules/auth/composables/useAuth'
import { config } from '@/shared/config/config'

const { t } = useI18n()
const router = useRouter()
const { isAuthenticated, user } = useAuth()

// If backend is disabled, redirect to home (offline mode)
if (!config.backend.enabled) {
  router.replace({ name: 'home' })
}
</script>

<template>
  <LandingLayout>
    <div class="max-w-2xl w-full space-y-8 text-center">
      <!-- Logo/Icon -->
      <div class="flex justify-center">
        <div class="rounded-full bg-primary/10 p-8">
          <FileText class="size-20 text-primary" />
        </div>
      </div>

      <!-- Heading -->
      <div class="space-y-4">
        <p v-if="isAuthenticated && user" class="text-2xl font-semibold text-muted-foreground">
          {{ t('landing.welcomeBack', { name: user.name }) }}
        </p>
        <h1 class="text-5xl font-bold tracking-tight">
          {{ t('landing.title', 'CareerHub') }}
        </h1>
        <p class="text-xl text-muted-foreground max-w-lg mx-auto">
          {{ t('landing.subtitle', 'One professional profile. As many tailored CVs as you need.') }}
        </p>
      </div>
    </div>

    <!-- Features -->
    <div class="max-w-2xl w-full space-y-8 text-center">
      <div class="grid grid-cols-1 md:grid-cols-3 py-4 gap-6">
        <div class="space-y-2">
          <h3 class="font-semibold text-lg">
            {{ t('landing.feature1.title', 'Build') }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ t('landing.feature1.description', 'Capture your experience, projects, and skills once') }}
          </p>
        </div>
        <div class="space-y-2">
          <h3 class="font-semibold text-lg">
            {{ t('landing.feature2.title', 'Curate') }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ t('landing.feature2.description', 'Select what matters for each application') }}
          </p>
        </div>
        <div class="space-y-2">
          <h3 class="font-semibold text-lg">
            {{ t('landing.feature3.title', 'Share') }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ t('landing.feature3.description', 'Generate a tailored CV or share your public profile link') }}
          </p>
        </div>
      </div>
    </div>
  </LandingLayout>
</template>
