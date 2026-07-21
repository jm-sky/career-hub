<script setup lang="ts">
import { ArrowDown, ArrowUp, Pencil, Plus, Star, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import AchievementFormDialog from '@/modules/career/components/AchievementFormDialog.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import { useAchievements } from '@/modules/career/composables/useAchievements'
import type { Achievement, CreateAchievementData, UpdateAchievementData } from '@/modules/career/types/achievement.type'

const { t } = useI18n()

const {
  achievements,
  isLoading,
  isError,
  createAchievement,
  isCreating,
  updateAchievement,
  isUpdating,
  deleteAchievement,
  isDeleting,
  reorderAchievements,
} = useAchievements()

const sortedAchievements = computed(() => [...(achievements.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingAchievement = ref<Achievement | null>(null)

const deleteOpen = ref(false)
const deletingAchievement = ref<Achievement | null>(null)

function openCreate() {
  editingAchievement.value = null
  formOpen.value = true
}

function openEdit(achievement: Achievement) {
  editingAchievement.value = achievement
  formOpen.value = true
}

async function handleSubmit(data: CreateAchievementData | UpdateAchievementData) {
  try {
    if (editingAchievement.value) {
      await updateAchievement({ id: editingAchievement.value.id, data: data as UpdateAchievementData })
    } else {
      await createAchievement(data as CreateAchievementData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(achievement: Achievement) {
  deletingAchievement.value = achievement
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingAchievement.value) return
  try {
    await deleteAchievement(deletingAchievement.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedAchievements.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(achievement => achievement.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderAchievements(ids)
  } catch {
    toast.error(t('errors.generic'))
  }
}
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-6 max-w-3xl">
      <div class="flex items-start justify-between gap-4">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ t('career.achievements.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.achievements.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.achievements.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.achievements.page.error') }}
      </div>

      <Card v-else-if="!sortedAchievements.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <Star class="size-8" />
          <p>{{ t('career.achievements.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="(achievement, index) in sortedAchievements" :key="achievement.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle class="flex items-center gap-2">
                {{ achievement.title }}
                <Badge v-if="achievement.category" variant="secondary">
                  {{ t(`career.achievements.categoryOptions.${achievement.category}`) }}
                </Badge>
              </CardTitle>
              <p v-if="achievement.date" class="text-xs text-muted-foreground">
                {{ achievement.date }}
              </p>
            </div>
            <div class="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                :disabled="index === 0"
                @click="move(index, -1)"
              >
                <ArrowUp class="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                :disabled="index === sortedAchievements.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(achievement)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(achievement)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent v-if="achievement.description">
            <p class="text-sm">
              {{ achievement.description }}
            </p>
          </CardContent>
        </Card>
      </div>
    </div>

    <AchievementFormDialog
      v-model:open="formOpen"
      :achievement="editingAchievement"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.achievements.deleteConfirm.title')"
      :description="t('career.achievements.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
