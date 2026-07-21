<script setup lang="ts">
import AppFooter from '@/components/layout/AppFooter.vue'
import DarkModeToggle from '@/shared/components/DarkModeToggle.vue'
import LocaleToggle from '@/shared/i18n/components/LocaleToggle.vue'
</script>

<template>
  <div class="relative flex min-h-screen flex-col bg-transparent">
    <!-- Fixed controls in top right -->
    <nav class="glass-surface fixed top-2 right-2 z-10 flex gap-2 rounded-xl border border-border bg-card/70 p-2">
      <LocaleToggle />
      <DarkModeToggle />
    </nav>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center justify-center gap-8 p-4">
      <slot />
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

