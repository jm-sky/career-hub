<script setup lang="ts">
import { Briefcase, Info, Sparkles, UserRound } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar'
import { CareerRoutePaths } from '@/modules/career/routes'
import { PublicRoutePaths } from '@/router/publicRoutes'

const { t } = useI18n()
</script>

<template>
  <Sidebar collapsible="icon">
    <SidebarContent class="overflow-x-hidden max-h-[90vh] overflow-y-auto">
      <SidebarMenu>
        <SidebarMenuItem>
          <RouterLink v-slot="{ href, navigate, isActive }" :to="CareerRoutePaths.profileEdit" custom>
            <SidebarMenuButton
              :is-active="isActive"
              as="a"
              :href="href"
              @click="navigate"
            >
              <UserRound class="size-4" />
              <span>{{ t('career.profile.page.title') }}</span>
            </SidebarMenuButton>
          </RouterLink>
        </SidebarMenuItem>

        <SidebarMenuItem>
          <RouterLink v-slot="{ href, navigate, isActive }" :to="CareerRoutePaths.experiences" custom>
            <SidebarMenuButton
              :is-active="isActive"
              as="a"
              :href="href"
              @click="navigate"
            >
              <Briefcase class="size-4" />
              <span>{{ t('career.experiences.page.title') }}</span>
            </SidebarMenuButton>
          </RouterLink>
        </SidebarMenuItem>

        <SidebarMenuItem>
          <RouterLink v-slot="{ href, navigate, isActive }" :to="CareerRoutePaths.skills" custom>
            <SidebarMenuButton
              :is-active="isActive"
              as="a"
              :href="href"
              @click="navigate"
            >
              <Sparkles class="size-4" />
              <span>{{ t('career.skills.page.title') }}</span>
            </SidebarMenuButton>
          </RouterLink>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarContent>

    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <RouterLink v-slot="{ href, navigate, isActive }" :to="PublicRoutePaths.about" custom>
            <SidebarMenuButton
              :is-active="isActive"
              as="a"
              :href="href"
              @click="navigate"
            >
              <Info class="size-4" />
              <span>{{ t('common.pages.about', 'About') }}</span>
            </SidebarMenuButton>
          </RouterLink>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>

    <SidebarRail />
  </Sidebar>
</template>
