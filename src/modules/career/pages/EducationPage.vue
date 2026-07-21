<script setup lang="ts">
import { ArrowDown, ArrowUp, GraduationCap, Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import EducationFormDialog from '@/modules/career/components/EducationFormDialog.vue'
import { useEducation } from '@/modules/career/composables/useEducation'
import type { CreateEducationData, Education, UpdateEducationData } from '@/modules/career/types/education.type'

const { t } = useI18n()

const {
  education,
  isLoading,
  isError,
  createEducation,
  isCreating,
  updateEducation,
  isUpdating,
  deleteEducation,
  isDeleting,
  reorderEducation,
} = useEducation()

const sortedEducation = computed(() => [...(education.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingEducation = ref<Education | null>(null)

const deleteOpen = ref(false)
const deletingEducation = ref<Education | null>(null)

function openCreate() {
  editingEducation.value = null
  formOpen.value = true
}

function openEdit(entry: Education) {
  editingEducation.value = entry
  formOpen.value = true
}

async function handleSubmit(data: CreateEducationData | UpdateEducationData) {
  try {
    if (editingEducation.value) {
      await updateEducation({ id: editingEducation.value.id, data: data as UpdateEducationData })
    } else {
      await createEducation(data as CreateEducationData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(entry: Education) {
  deletingEducation.value = entry
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingEducation.value) return
  try {
    await deleteEducation(deletingEducation.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedEducation.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(entry => entry.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderEducation(ids)
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
            {{ t('career.education.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.education.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.education.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.education.page.error') }}
      </div>

      <Card v-else-if="!sortedEducation.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <GraduationCap class="size-8" />
          <p>{{ t('career.education.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="(entry, index) in sortedEducation" :key="entry.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle>{{ entry.degree }}</CardTitle>
              <p class="text-sm text-muted-foreground">
                {{ entry.institution }}
                <span v-if="entry.fieldOfStudy"> &middot; {{ entry.fieldOfStudy }}</span>
              </p>
              <p class="text-xs text-muted-foreground">
                {{ entry.startDate }} &ndash; {{ entry.endDate ?? t('career.education.fields.present') }}
                <span v-if="entry.grade"> &middot; {{ entry.grade }}</span>
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
                :disabled="index === sortedEducation.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(entry)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(entry)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent v-if="entry.description">
            <p class="text-sm">
              {{ entry.description }}
            </p>
          </CardContent>
        </Card>
      </div>
    </div>

    <EducationFormDialog
      v-model:open="formOpen"
      :education="editingEducation"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.education.deleteConfirm.title')"
      :description="t('career.education.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
