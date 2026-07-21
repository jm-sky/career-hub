<script setup lang="ts">
import LogoText from '@/components/ui/LogoText.vue'
import { PublicRouteNames } from '@/router/publicRoutes'
import DarkModeToggle from '@/shared/components/DarkModeToggle.vue'
import LocaleToggle from '@/shared/i18n/components/LocaleToggle.vue'

// Default layout for public pages (no authentication required)
</script>

<template>
  <div class="min-h-screen bg-transparent">
    <nav class="glass-surface border-b border-border bg-card/70">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between">
          <div class="flex items-center">
            <RouterLink :to="{ name: PublicRouteNames.landing }" class="text-xl font-bold text-card-foreground">
              <LogoText />
            </RouterLink>
          </div>

          <div class="flex items-center space-x-4">
            <RouterLink
              to="/auth/login"
              class="text-sm text-foreground hover:text-primary"
            >
              Zaloguj się
            </RouterLink>
            <RouterLink
              to="/auth/register"
              class="rounded-full bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/80"
            >
              Zarejestruj się
            </RouterLink>
            <LocaleToggle />
            <DarkModeToggle />
          </div>
        </div>
      </div>
    </nav>

    <main>
      <slot />
    </main>

    <footer class="bg-card border-t border-border mt-auto">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-muted-foreground">
          &copy; 2025 MyApp. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>
