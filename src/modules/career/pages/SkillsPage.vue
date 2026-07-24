<script setup lang="ts">
import { Pencil, Plus, Sparkles, Star, Trash2 } from 'lucide-vue-next'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import DeleteConfirmDialog from '@/modules/career/components/DeleteConfirmDialog.vue'
import SkillFormDialog from '@/modules/career/components/SkillFormDialog.vue'
import { useSkills } from '@/modules/career/composables/useSkills'
import { useHandleError } from '@/shared/composables/useHandleError'
import type { CreateSkillData, Skill, UpdateSkillData } from '@/modules/career/types/skill.type'

const { t } = useI18n()
const { handleError } = useHandleError()

const {
  skills,
  isLoading,
  isError,
  createSkill,
  isCreating,
  updateSkill,
  isUpdating,
  deleteSkill,
  isDeleting,
  suggestSkills,
  isSuggestingSkills,
} = useSkills()

const suggestOpen = ref(false)
const suggestRole = ref('')
const suggestedSkills = ref<string[]>([])

async function handleSuggestSkills() {
  const role = suggestRole.value.trim()
  if (!role) return
  try {
    suggestedSkills.value = await suggestSkills({ role })
  } catch (error) {
    handleError(error, { fallbackMessage: t('career.ai.error.accessDenied') })
  }
}

async function addSuggestedSkill(name: string) {
  try {
    await createSkill({ technologyName: name, level: 3 })
    suggestedSkills.value = suggestedSkills.value.filter(item => item !== name)
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

const formOpen = ref(false)
const editingSkill = ref<Skill | null>(null)

const deleteOpen = ref(false)
const deletingSkill = ref<Skill | null>(null)

function openCreate() {
  editingSkill.value = null
  formOpen.value = true
}

function openEdit(skill: Skill) {
  editingSkill.value = skill
  formOpen.value = true
}

async function handleSubmit(data: CreateSkillData | UpdateSkillData) {
  try {
    if (editingSkill.value) {
      await updateSkill({ id: editingSkill.value.id, data: data as UpdateSkillData })
    } else {
      await createSkill(data as CreateSkillData)
    }
    formOpen.value = false
    toast.success(t('career.profile.page.save'))
  } catch {
    toast.error(t('errors.generic'))
  }
}

function openDelete(skill: Skill) {
  deletingSkill.value = skill
  deleteOpen.value = true
}

async function handleDelete() {
  if (!deletingSkill.value) return
  try {
    await deleteSkill(deletingSkill.value.id)
    deleteOpen.value = false
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
            {{ t('career.skills.page.title') }}
          </h1>
          <p class="text-muted-foreground">
            {{ t('career.skills.page.subtitle') }}
          </p>
        </div>
        <div class="flex items-center gap-2">
          <Button variant="outline" @click="suggestOpen = !suggestOpen">
            <Sparkles class="size-4" />
            {{ t('career.ai.suggestSkills.button') }}
          </Button>
          <Button @click="openCreate">
            <Plus class="size-4" />
            {{ t('career.skills.page.add') }}
          </Button>
        </div>
      </div>

      <Card v-if="suggestOpen">
        <CardContent class="space-y-3 pt-6">
          <p class="text-sm font-medium">
            {{ t('career.ai.suggestSkills.title') }}
          </p>
          <div class="flex gap-2">
            <Input
              v-model="suggestRole"
              :placeholder="t('career.ai.suggestSkills.rolePlaceholder')"
              @keydown.enter.prevent="handleSuggestSkills"
            />
            <Button
              type="button"
              :disabled="!suggestRole.trim()"
              :loading="isSuggestingSkills"
              @click="handleSuggestSkills"
            >
              {{ t('career.ai.suggestSkills.button') }}
            </Button>
          </div>
          <p v-if="!suggestedSkills.length" class="text-sm text-muted-foreground">
            {{ t('career.ai.suggestSkills.empty') }}
          </p>
          <div v-else class="flex flex-wrap gap-2">
            <Badge
              v-for="name in suggestedSkills"
              :key="name"
              variant="secondary"
              class="cursor-pointer gap-1"
              @click="addSuggestedSkill(name)"
            >
              <Plus class="size-3" />
              {{ name }}
            </Badge>
          </div>
        </CardContent>
      </Card>

      <div v-if="isLoading" class="space-y-4">
        <div class="h-16 bg-muted rounded animate-pulse" />
        <div class="h-16 bg-muted rounded animate-pulse" />
      </div>

      <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
        {{ t('career.skills.page.error') }}
      </div>

      <Card v-else-if="!skills?.length">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center text-muted-foreground">
          <Sparkles class="size-8" />
          <p>{{ t('career.skills.page.empty') }}</p>
        </CardContent>
      </Card>

      <Card v-else>
        <CardContent class="divide-y p-0">
          <div
            v-for="skill in skills"
            :key="skill.id"
            class="flex items-center justify-between gap-4 p-4"
          >
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="font-medium">{{ skill.technology.name }}</span>
                <Badge v-if="skill.isPrimary" variant="default">
                  {{ t('career.skills.fields.isPrimary') }}
                </Badge>
              </div>
              <div class="flex items-center gap-1 text-muted-foreground">
                <Star
                  v-for="n in 5"
                  :key="n"
                  class="size-3.5"
                  :class="n <= skill.level ? 'fill-current text-amber-500' : ''"
                />
                <span v-if="skill.yearsOfExperience" class="ml-2 text-xs">
                  {{ t('career.skills.fields.yearsOfExperienceShort', { years: skill.yearsOfExperience }) }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-1">
              <Button variant="ghost" size="icon" @click="openEdit(skill)">
                <Pencil class="size-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="openDelete(skill)">
                <Trash2 class="size-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <SkillFormDialog
      v-model:open="formOpen"
      :skill="editingSkill"
      :saving="isCreating || isUpdating"
      @submit="handleSubmit"
    />

    <DeleteConfirmDialog
      v-model:open="deleteOpen"
      :title="t('career.skills.deleteConfirm.title')"
      :description="t('career.skills.deleteConfirm.description')"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </AuthenticatedLayout>
</template>
