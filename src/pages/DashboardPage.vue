<script setup lang="ts">
import { LogIn, UserCircle2, UserPlus } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import ButtonLink from '@/components/ui/button-link/ButtonLink.vue'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import { useAuth } from '@/modules/auth/composables/useAuth'
import { AuthRoutePaths } from '@/modules/auth/config/routes'
import UpgradePromptBanner from '@/modules/billing/components/UpgradePromptBanner.vue'
import { config } from '@/shared/config/config'

const { t } = useI18n()
const { isAuthenticated } = useAuth()
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-8">
      <!-- Upgrade Prompt Banner (only for authenticated FREE users) -->
      <UpgradePromptBanner v-if="isAuthenticated && config.backend.enabled" />

      <!-- Header -->
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

      <!-- Actions -->
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
    </div>
  </AuthenticatedLayout>
</template>
