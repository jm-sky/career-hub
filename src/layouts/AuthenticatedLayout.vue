<script setup lang="ts">
import AppFooter from '@/components/layout/AppFooter.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

defineProps<{
  cardClass?: HTMLAttributes['class']
}>()
</script>

<template>
  <SidebarProvider class="bg-transparent">
    <AppSidebar class="mt-(--header-height)" />
    <SidebarInset class="min-w-0 bg-transparent pt-14">
      <div class="flex min-h-screen min-w-0 w-full max-w-full flex-col overflow-x-hidden bg-transparent">
        <!-- Top Bar -->
        <AppHeader />

        <!-- Main Content -->
        <main class="mx-auto w-full min-w-0 max-w-7xl flex-1 px-2 py-6 sm:px-6 lg:px-8">
          <div
            :class="cn(
              'glass-surface w-full min-w-0 max-w-full rounded-2xl border border-border bg-glass p-4 shadow-none sm:p-6',
              cardClass,
            )"
          >
            <slot />
          </div>
        </main>

        <!-- Footer -->
        <AppFooter />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
