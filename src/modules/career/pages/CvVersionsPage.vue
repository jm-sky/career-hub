<script setup lang="ts">
import { Download, FileStack, Pencil, Play, Plus, Trash2 } from 'lucide-vue-next'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import CvVersionFormDialog from '@/modules/career/components/CvVersionFormDialog.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import { useCvVersions } from '@/modules/career/composables/useCvVersions'
import type { CreateCvVersionData, CvVersion, UpdateCvVersionData } from '@/modules/career/types/cvVersion.type'

const { t } = useI18n()

const {
  cvVersions,
  isLoading,
  isError,
  createCvVersion,
  isCreating,
  updateCvVersion,
  isUpdating,
  deleteCvVersion,
  isDeleting,
  generateCvVersion,
} = useCvVersions()

const formOpen = ref(false)
const editingCvVersion = ref<CvVersion | null>(null)

const deleteOpen = ref(false)
const deletingCvVersion = ref<CvVersion | null>(null)

function openCreate() {
  editingCvVersion.value = null
  formOpen.value = true
}

function openEdit(cvVersion: CvVersion) {
  editingCvVersion.value = cvVersion
  formOpen.value = true
}

async function handleSubmit(data: CreateCvVersionData | UpdateCvVersionData) {
  try {
    if (editingCvVersion.value) {
      await updateCvVersion({ id: editingCvVersion.value.id, data: data as UpdateCvVersionData })
    } else {
      await createCvVersion(data as CreateCvVersionData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(cvVersion: CvVersion) {
  deletingCvVersion.value = cvVersion
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingCvVersion.value) return
  try {
    await deleteCvVersion(deletingCvVersion.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function handleGenerate(cvVersion: CvVersion) {
  try {
    await generateCvVersion(cvVersion.id)
    toast.info(t('career.cvVersions.page.generateStub'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function handleDownload() {
  toast.info(t('career.cvVersions.page.downloadStub'))
}
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-6">
      <div class="flex items-start justify-between gap-4">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ t('career.cvVersions.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.cvVersions.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.cvVersions.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.cvVersions.page.error') }}
      </div>

      <Card v-else-if="!cvVersions?.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <FileStack class="size-8" />
          <p>{{ t('career.cvVersions.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="cvVersion in cvVersions" :key="cvVersion.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle class="flex items-center gap-2">
                {{ cvVersion.name }}
                <Badge v-if="cvVersion.isDefault" variant="default">
                  {{ t('career.cvVersions.fields.isDefault') }}
                </Badge>
              </CardTitle>
              <p class="text-sm text-muted-foreground">
                {{ t(`career.cvVersions.templateOptions.${cvVersion.template}`, cvVersion.template) }}
              </p>
            </div>
            <div class="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                :title="t('career.cvVersions.page.generate')"
                @click="handleGenerate(cvVersion)"
              >
                <Play class="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                :title="t('career.cvVersions.page.download')"
                @click="handleDownload"
              >
                <Download class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(cvVersion)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(cvVersion)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
        </Card>
      </div>
    </div>

    <CvVersionFormDialog
      v-model:open="formOpen"
      :cv-version="editingCvVersion"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.cvVersions.deleteConfirm.title')"
      :description="t('career.cvVersions.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
