<script setup lang="ts">
import { useRoute } from 'vue-router'
import GuestLayoutFooter from '@/components/layout/GuestLayoutFooter.vue'
import LogoText from '@/components/ui/LogoText.vue'
import { PublicRouteNames } from '@/router/publicRoutes'
import DarkModeToggle from '@/shared/components/DarkModeToggle.vue'
import LocaleToggle from '@/shared/i18n/components/LocaleToggle.vue'

// Auth layout for login, register, forgot password pages
const route = useRoute()
const layoutActionsComponent = route.meta.layoutActionsComponent
</script>

<template>
  <div class="relative flex min-h-screen flex-col bg-transparent">
    <nav class="glass-surface fixed top-2 right-2 z-10 flex gap-2 rounded-xl border border-border bg-card/70 p-2">
      <slot name="actions">
        <component :is="layoutActionsComponent" v-if="layoutActionsComponent" />
      </slot>
      <LocaleToggle />
      <DarkModeToggle />
    </nav>

    <main class="flex-1 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative z-0">
      <div class="mx-auto text-center mb-8">
        <RouterLink :to="{ name: PublicRouteNames.landing }" class="block hover:opacity-80 hover:scale-105 transition-all">
          <LogoText class="text-3xl drop-shadow" />
        </RouterLink>
      </div>

      <slot />
    </main>

    <GuestLayoutFooter />
  </div>
</template>
