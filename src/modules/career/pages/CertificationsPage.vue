<script setup lang="ts">
import { ArrowDown, ArrowUp, Award, Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import CertificationFormDialog from '@/modules/career/components/CertificationFormDialog.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import { useCertifications } from '@/modules/career/composables/useCertifications'
import type { Certification, CreateCertificationData, UpdateCertificationData } from '@/modules/career/types/certification.type'

const { t } = useI18n()

const {
  certifications,
  isLoading,
  isError,
  createCertification,
  isCreating,
  updateCertification,
  isUpdating,
  deleteCertification,
  isDeleting,
  reorderCertifications,
} = useCertifications()

const sortedCertifications = computed(() => [...(certifications.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingCertification = ref<Certification | null>(null)

const deleteOpen = ref(false)
const deletingCertification = ref<Certification | null>(null)

function openCreate() {
  editingCertification.value = null
  formOpen.value = true
}

function openEdit(certification: Certification) {
  editingCertification.value = certification
  formOpen.value = true
}

async function handleSubmit(data: CreateCertificationData | UpdateCertificationData) {
  try {
    if (editingCertification.value) {
      await updateCertification({ id: editingCertification.value.id, data: data as UpdateCertificationData })
    } else {
      await createCertification(data as CreateCertificationData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(certification: Certification) {
  deletingCertification.value = certification
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingCertification.value) return
  try {
    await deleteCertification(deletingCertification.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedCertifications.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(certification => certification.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderCertifications(ids)
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
            {{ t('career.certifications.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.certifications.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.certifications.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.certifications.page.error') }}
      </div>

      <Card v-else-if="!sortedCertifications.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <Award class="size-8" />
          <p>{{ t('career.certifications.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="(certification, index) in sortedCertifications" :key="certification.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle class="flex items-center gap-2">
                {{ certification.name }}
                <Badge v-if="certification.isExpired" variant="destructive">
                  {{ t('career.certifications.expired') }}
                </Badge>
              </CardTitle>
              <p class="text-sm text-muted-foreground">
                {{ certification.issuingOrganization }}
              </p>
              <p class="text-xs text-muted-foreground">
                {{ certification.issueDate }}
                <span v-if="certification.expiryDate"> &ndash; {{ certification.expiryDate }}</span>
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
                :disabled="index === sortedCertifications.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(certification)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(certification)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
        </Card>
      </div>
    </div>

    <CertificationFormDialog
      v-model:open="formOpen"
      :certification="editingCertification"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.certifications.deleteConfirm.title')"
      :description="t('career.certifications.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
