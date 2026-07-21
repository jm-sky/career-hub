<script setup lang="ts">
import { useRoute } from 'vue-router'
import GuestLayoutFooter from '@/components/layout/GuestLayoutFooter.vue'
import LogoText from '@/components/ui/LogoText.vue'
import { PublicRouteNames } from '@/router/publicRoutes'
import DarkModeToggle from '@/shared/components/DarkModeToggle.vue'
import LocaleToggle from '@/shared/i18n/components/LocaleToggle.vue'

defineProps<{
  backgroundImage?: string
}>()

const route = useRoute()
const layoutActionsComponent = route.meta.layoutActionsComponent
</script>

<template>
  <div class="relative flex min-h-screen flex-col bg-transparent">
    <!-- Background image with smooth transitions -->
    <div
      v-if="backgroundImage"
      class="absolute inset-0 bg-cover bg-center transition-opacity duration-500"
      :style="{ backgroundImage: `url(${backgroundImage})` }"
    >
      <div class="absolute inset-0 bg-black/40 transition-colors duration-500 dark:bg-black/60" />
    </div>

    <!-- Fixed floating controls -->
    <nav class="glass-surface fixed top-2 right-2 z-10 flex gap-2 rounded-xl border border-border bg-card/70 p-2">
      <slot name="actions">
        <component :is="layoutActionsComponent" v-if="layoutActionsComponent" />
      </slot>
      <LocaleToggle />
      <DarkModeToggle />
    </nav>

    <!-- Main content -->
    <main class="relative z-0 flex flex-1 flex-col items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
      <!-- Logo -->
      <div class="mx-auto mb-8 text-center">
        <RouterLink :to="{ name: PublicRouteNames.landing }" class="block transition-all hover:scale-105 hover:opacity-80">
          <LogoText class="text-3xl drop-shadow" />
        </RouterLink>
      </div>

      <!-- Content with glass-morphism -->
      <div class="glass-surface w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-none">
        <slot />
      </div>
    </main>

    <!-- Footer -->
    <GuestLayoutFooter />
  </div>
</template>
