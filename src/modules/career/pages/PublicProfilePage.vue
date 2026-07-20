<script setup lang="ts">
import { HttpStatusCode, isAxiosError } from 'axios'
import { UserRound } from 'lucide-vue-next'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { Card, CardContent } from '@/components/ui/card'
import PublicLayout from '@/layouts/PublicLayout.vue'
import { usePublicProfile } from '@/modules/career/composables/useProfile'

const route = useRoute()
const { t } = useI18n()

const slug = computed(() => route.params.slug as string)
const { data: profile, isLoading, isError, error } = usePublicProfile(slug.value)

const errorMessage = computed(() => {
  if (isAxiosError(error.value) && error.value.response?.status === HttpStatusCode.NotFound) {
    return t('career.publicProfile.not_found')
  }
  return t('career.publicProfile.error')
})
</script>

<template>
  <PublicLayout>
    <div class="max-w-2xl mx-auto py-12 px-4 space-y-6">
      <div v-if="isLoading" class="space-y-4">
        <div class="h-32 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-6 text-center">
        {{ errorMessage }}
      </div>

      <Card v-else-if="profile">
        <CardContent class="space-y-4 pt-6">
          <div class="flex items-center gap-4">
            <div class="rounded-full bg-primary/10 p-4">
              <UserRound class="size-10 text-primary" />
            </div>
            <div>
              <h1 v-if="profile.headline" class="text-2xl font-bold">
                {{ profile.headline }}
              </h1>
              <p v-if="profile.location" class="text-muted-foreground">
                {{ profile.location }}
              </p>
            </div>
          </div>
          <p v-if="profile.summary" class="text-muted-foreground whitespace-pre-wrap">
            {{ profile.summary }}
          </p>
        </CardContent>
      </Card>
    </div>
  </PublicLayout>
</template>
