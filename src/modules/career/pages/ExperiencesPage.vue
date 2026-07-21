<script setup lang="ts">
import { ArrowDown, ArrowUp, Briefcase, Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import ExperienceFormDialog from '@/modules/career/components/ExperienceFormDialog.vue'
import { useExperiences } from '@/modules/career/composables/useExperiences'
import type { CreateExperienceData, Experience, UpdateExperienceData } from '@/modules/career/types/experience.type'

const { t } = useI18n()

const {
  experiences,
  isLoading,
  isError,
  createExperience,
  isCreating,
  updateExperience,
  isUpdating,
  deleteExperience,
  isDeleting,
  reorderExperiences,
} = useExperiences()

const sortedExperiences = computed(() => [...(experiences.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingExperience = ref<Experience | null>(null)

const deleteOpen = ref(false)
const deletingExperience = ref<Experience | null>(null)

function openCreate() {
  editingExperience.value = null
  formOpen.value = true
}

function openEdit(experience: Experience) {
  editingExperience.value = experience
  formOpen.value = true
}

async function handleSubmit(data: CreateExperienceData | UpdateExperienceData) {
  try {
    if (editingExperience.value) {
      await updateExperience({ id: editingExperience.value.id, data: data as UpdateExperienceData })
    } else {
      await createExperience(data as CreateExperienceData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(experience: Experience) {
  deletingExperience.value = experience
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingExperience.value) return
  try {
    await deleteExperience(deletingExperience.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedExperiences.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(experience => experience.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderExperiences(ids)
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
            {{ t('career.experiences.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.experiences.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.experiences.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.experiences.page.error') }}
      </div>

      <Card v-else-if="!sortedExperiences.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <Briefcase class="size-8" />
          <p>{{ t('career.experiences.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="(experience, index) in sortedExperiences" :key="experience.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle>{{ experience.position }}</CardTitle>
              <p class="text-sm text-muted-foreground">
                {{ experience.companyName }}
                <span v-if="experience.employmentType"> &middot; {{ experience.employmentType }}</span>
              </p>
              <p class="text-xs text-muted-foreground">
                {{ experience.startDate }} &ndash;
                {{ experience.isCurrent ? t('career.experiences.fields.isCurrent') : experience.endDate }}
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
                :disabled="index === sortedExperiences.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(experience)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(experience)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent class="space-y-3">
            <p v-if="experience.description" class="text-sm">
              {{ experience.description }}
            </p>
            <ul v-if="experience.responsibilities.length" class="list-disc pl-5 text-sm space-y-1">
              <li v-for="(item, i) in experience.responsibilities" :key="i">
                {{ item }}
              </li>
            </ul>
            <div v-if="experience.technologies.length" class="flex flex-wrap gap-2">
              <Badge v-for="technology in experience.technologies" :key="technology.id" variant="secondary">
                {{ technology.name }}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <ExperienceFormDialog
      v-model:open="formOpen"
      :experience="editingExperience"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.experiences.deleteConfirm.title')"
      :description="t('career.experiences.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
