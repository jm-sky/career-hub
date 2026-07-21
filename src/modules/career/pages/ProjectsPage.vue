<script setup lang="ts">
import { ArrowDown, ArrowUp, FolderKanban, Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import ProjectFormDialog from '@/modules/career/components/ProjectFormDialog.vue'
import { useProjects } from '@/modules/career/composables/useProjects'
import type { CreateProjectData, Project, UpdateProjectData } from '@/modules/career/types/project.type'

const { t } = useI18n()

const {
  projects,
  isLoading,
  isError,
  createProject,
  isCreating,
  updateProject,
  isUpdating,
  deleteProject,
  isDeleting,
  reorderProjects,
} = useProjects()

const sortedProjects = computed(() => [...(projects.value ?? [])].sort((a, b) => a.displayOrder - b.displayOrder))

const formOpen = ref(false)
const editingProject = ref<Project | null>(null)

const deleteOpen = ref(false)
const deletingProject = ref<Project | null>(null)

function openCreate() {
  editingProject.value = null
  formOpen.value = true
}

function openEdit(project: Project) {
  editingProject.value = project
  formOpen.value = true
}

async function handleSubmit(data: CreateProjectData | UpdateProjectData) {
  try {
    if (editingProject.value) {
      await updateProject({ id: editingProject.value.id, data: data as UpdateProjectData })
    } else {
      await createProject(data as CreateProjectData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(project: Project) {
  deletingProject.value = project
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingProject.value) return
  try {
    await deleteProject(deletingProject.value.id)
    deleteOpen.value = false
  } catch {
    toast.error(t('errors.generic'))
  }
}

async function move(index: number, direction: -1 | 1) {
  const list = sortedProjects.value
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= list.length) return
  const ids = list.map(project => project.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await reorderProjects(ids)
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
            {{ t('career.projects.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.projects.page.subtitle') }}
          </p>
        </div>
        <Button @click="openCreate">
          <Plus class="size-4" />
          {{ t('career.projects.page.add') }}
        </Button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-24 bg-muted rounded animate-pulse" />
        <div class="h-24 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.projects.page.error') }}
      </div>

      <Card v-else-if="!sortedProjects.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <FolderKanban class="size-8" />
          <p>{{ t('career.projects.page.empty') }}</p>
        </CardContent>
      </Card>

      <div v-else class="space-y-4">
        <Card v-for="(project, index) in sortedProjects" :key="project.id">
          <CardHeader class="flex flex-row items-start justify-between gap-4 space-y-0">
            <div>
              <CardTitle>{{ project.name }}</CardTitle>
              <p class="text-sm text-muted-foreground">
                <span v-if="project.role">{{ project.role }} &middot; </span>
                <span v-if="project.isAnonymized">{{ project.anonymizedCompany ?? t('career.projects.anonymized') }}</span>
              </p>
              <p class="text-xs text-muted-foreground">
                {{ project.startDate }} &ndash;
                {{ project.isOngoing ? t('career.projects.fields.isOngoing') : project.endDate }}
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
                :disabled="index === sortedProjects.length - 1"
                @click="move(index, 1)"
              >
                <ArrowDown class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openEdit(project)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(project)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent class="space-y-3">
            <p v-if="project.description" class="text-sm">
              {{ project.description }}
            </p>
            <div v-if="project.technologies.length" class="flex flex-wrap gap-2">
              <Badge v-for="technology in project.technologies" :key="technology.id" variant="secondary">
                {{ technology.name }}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <ProjectFormDialog
      v-model:open="formOpen"
      :project="editingProject"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.projects.deleteConfirm.title')"
      :description="t('career.projects.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
