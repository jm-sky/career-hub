<script setup lang="ts">
import { ArrowDown, ArrowUp, Languages, Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import LanguageFormDialog from '@/modules/career/components/LanguageFormDialog.vue'
import { useLanguages } from '@/modules/career/composables/useLanguages'
import type { CreateLanguageData, Language, UpdateLanguageData } from '@/modules/career/types/language.type'

const { t } = useI18n()

const {
  languages,
  isLoading,
  isError,
  createLanguage,
  isCreating,
  updateLanguage,
  isUpdating,
  deleteLanguage,
  isDeleting,
  reorderLanguages,
} = useLanguages()

const sortedLanguages = computed(() => [...(languages.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingLanguage = ref<Language | null>(null)

const deleteOpen = ref(false)
const deletingLanguage = ref<Language | null>(null)

function openCreate() {
  editingLanguage.value = null
  formOpen.value = true
}

function openEdit(entry: Language) {
  editingLanguage.value = entry
  formOpen.value = true
}

async function handleSubmit(data: CreateLanguageData | UpdateLanguageData) {
  try {
    if (editingLanguage.value) {
      await updateLanguage({ id: editingLanguage.value.id, data: data as UpdateLanguageData })
    } else {
      await createLanguage(data as CreateLanguageData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(entry: Language) {
  deletingLanguage.value = entry
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingLanguage.value) return
  try {
    await deleteLanguage(deletingLanguage.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedLanguages.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(entry => entry.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderLanguages(ids)
  } catch {
    toast.error(t('errors.generic'))
  }
}
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-6">
      <div class="flex items-start justify-between gap-4">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ t('career.languages.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.languages.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.languages.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.languages.page.error') }}
      </div>

      <Card v-else-if="!sortedLanguages.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <Languages class="size-8" />
          <p>{{ t('career.languages.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card
          v-for="(entry, index) in sortedLanguages"
          :key="entry.id"
        >
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle>{{ entry.name }}</CardTitle>
              <p class="text-sm text-muted-foreground">
                {{ t(`career.languages.levelOptions.${entry.level}`) }}
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
                :disabled="index === sortedLanguages.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                @click="openEdit(entry)"
              >
                <Pencil class="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                @click="openDelete(entry)"
              >
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

    <LanguageFormDialog
      v-model:open="formOpen"
      :language="editingLanguage"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.languages.deleteConfirm.title')"
      :description="t('career.languages.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
