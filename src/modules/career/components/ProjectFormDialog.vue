<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import Select from '@/components/ui/select/Select.vue'
import SelectContent from '@/components/ui/select/SelectContent.vue'
import SelectGroup from '@/components/ui/select/SelectGroup.vue'
import SelectItem from '@/components/ui/select/SelectItem.vue'
import SelectTrigger from '@/components/ui/select/SelectTrigger.vue'
import SelectValue from '@/components/ui/select/SelectValue.vue'
import { Textarea } from '@/components/ui/textarea'
import StringListInput from '@/modules/career/components/StringListInput.vue'
import TechnologyTagInput from '@/modules/career/components/TechnologyTagInput.vue'
import { useExperiencesQuery } from '@/modules/career/composables/useExperiences'
import { projectSchema } from '@/modules/career/validation/project.schema'
import type { CreateProjectData, Project, UpdateProjectData } from '@/modules/career/types/project.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  project?: Project | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateProjectData | UpdateProjectData]
}>()

const isEditing = computed(() => !!props.project)

const achievements = ref<string[]>([])
const challenges = ref<string[]>([])
const clients = ref<string[]>([])
const technologies = ref<string[]>([])
const experienceIds = ref<string[]>([])

const experiencesQuery = useExperiencesQuery()

const { handleSubmit, resetForm, values } = useForm({
  validationSchema: toTypedSchema(projectSchema),
  initialValues: {
    name: '',
    description: '',
    role: '',
    startDate: '',
    endDate: '',
    isOngoing: false,
    isAnonymized: false,
    anonymizedCompany: '',
    status: 'ACTIVE' as const,
    category: undefined,
    teamSize: undefined,
    durationMonths: undefined,
    usersCount: undefined,
    budgetRange: '',
    demo: '',
    github: '',
    docs: '',
    visibility: 'PRIVATE' as const,
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const project = props.project
  resetForm({
    values: {
      name: project?.name ?? '',
      description: project?.description ?? '',
      role: project?.role ?? '',
      startDate: project?.startDate ?? '',
      endDate: project?.endDate ?? '',
      isOngoing: project?.isOngoing ?? false,
      isAnonymized: project?.isAnonymized ?? false,
      anonymizedCompany: project?.anonymizedCompany ?? '',
      status: project?.status ?? 'ACTIVE',
      category: project?.category ?? undefined,
      teamSize: project?.teamSize ?? undefined,
      durationMonths: project?.durationMonths ?? undefined,
      usersCount: project?.usersCount ?? undefined,
      budgetRange: project?.budgetRange ?? '',
      demo: project?.links?.demo ?? '',
      github: project?.links?.github ?? '',
      docs: project?.links?.docs ?? '',
      visibility: project?.visibility ?? 'PRIVATE',
    },
  })
  achievements.value = project?.achievements ? [...project.achievements] : []
  challenges.value = project?.challenges ? [...project.challenges] : []
  clients.value = project?.clients ? [...project.clients] : []
  technologies.value = project?.technologies ? project.technologies.map(technology => technology.name) : []
  experienceIds.value = project?.experienceIds ? [...project.experienceIds] : []
})

function toggleExperience(id: string) {
  experienceIds.value = experienceIds.value.includes(id)
    ? experienceIds.value.filter(existing => existing !== id)
    : [...experienceIds.value, id]
}

const onSubmit = handleSubmit((formValues) => {
  emit('submit', {
    name: formValues.name,
    description: formValues.description || null,
    role: formValues.role || null,
    startDate: formValues.startDate,
    endDate: formValues.isOngoing ? null : (formValues.endDate || null),
    isOngoing: formValues.isOngoing,
    isAnonymized: formValues.isAnonymized,
    anonymizedCompany: formValues.anonymizedCompany || null,
    status: formValues.status,
    category: formValues.category ?? null,
    achievements: achievements.value,
    challenges: challenges.value,
    clients: clients.value,
    teamSize: formValues.teamSize ?? null,
    durationMonths: formValues.durationMonths ?? null,
    usersCount: formValues.usersCount ?? null,
    budgetRange: formValues.budgetRange || null,
    links: {
      demo: formValues.demo || null,
      github: formValues.github || null,
      docs: formValues.docs || null,
    },
    visibility: formValues.visibility,
    technologies: technologies.value,
    experienceIds: experienceIds.value,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.projects.form.editTitle') : t('career.projects.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.projects.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="name">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.name') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="role">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.role') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('career.projects.fields.description') }}</FormLabel>
            <FormControl>
              <Textarea v-bind="componentField" rows="3" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="startDate">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.startDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="endDate">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.endDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" :disabled="values.isOngoing" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="isOngoing">
          <FormItem class="flex items-center gap-2 space-y-0">
            <FormControl>
              <Checkbox
                :model-value="componentField.modelValue"
                @update:model-value="componentField['onUpdate:modelValue']"
              />
            </FormControl>
            <FormLabel class="font-normal">
              {{ t('career.projects.fields.isOngoing') }}
            </FormLabel>
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="isAnonymized">
          <FormItem class="flex items-center gap-2 space-y-0">
            <FormControl>
              <Checkbox
                :model-value="componentField.modelValue"
                @update:model-value="componentField['onUpdate:modelValue']"
              />
            </FormControl>
            <FormLabel class="font-normal">
              {{ t('career.projects.fields.isAnonymized') }}
            </FormLabel>
          </FormItem>
        </FormField>

        <FormField v-if="values.isAnonymized" v-slot="{ componentField }" name="anonymizedCompany">
          <FormItem>
            <FormLabel>{{ t('career.projects.fields.anonymizedCompany') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" :placeholder="t('career.projects.fields.anonymizedCompanyPlaceholder')" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="status">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.status') }}</FormLabel>
              <FormControl>
                <Select v-bind="componentField">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="ACTIVE">
                        {{ t('career.projects.statusOptions.ACTIVE') }}
                      </SelectItem>
                      <SelectItem value="STAGING">
                        {{ t('career.projects.statusOptions.STAGING') }}
                      </SelectItem>
                      <SelectItem value="ARCHIVED">
                        {{ t('career.projects.statusOptions.ARCHIVED') }}
                      </SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="category">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.category') }}</FormLabel>
              <FormControl>
                <Select v-bind="componentField">
                  <SelectTrigger>
                    <SelectValue :placeholder="t('career.projects.fields.categoryPlaceholder')" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="DEMO">
                        {{ t('career.projects.categoryOptions.DEMO') }}
                      </SelectItem>
                      <SelectItem value="INTERNAL">
                        {{ t('career.projects.categoryOptions.INTERNAL') }}
                      </SelectItem>
                      <SelectItem value="PRODUCTION">
                        {{ t('career.projects.categoryOptions.PRODUCTION') }}
                      </SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <div class="space-y-2">
          <Label>{{ t('career.projects.fields.achievements') }}</Label>
          <StringListInput v-model="achievements" :placeholder="t('career.projects.fields.achievementsPlaceholder')" />
        </div>

        <div class="space-y-2">
          <Label>{{ t('career.projects.fields.challenges') }}</Label>
          <StringListInput v-model="challenges" :placeholder="t('career.projects.fields.challengesPlaceholder')" />
        </div>

        <div class="space-y-2">
          <Label>{{ t('career.projects.fields.clients') }}</Label>
          <StringListInput v-model="clients" :placeholder="t('career.projects.fields.clientsPlaceholder')" />
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="teamSize">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.teamSize') }}</FormLabel>
              <FormControl>
                <Input type="number" min="0" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="durationMonths">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.durationMonths') }}</FormLabel>
              <FormControl>
                <Input type="number" min="0" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="usersCount">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.usersCount') }}</FormLabel>
              <FormControl>
                <Input type="number" min="0" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="budgetRange">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.budgetRange') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" :placeholder="t('career.projects.fields.budgetRangePlaceholder')" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <div class="space-y-4">
          <p class="text-sm font-medium">
            {{ t('career.projects.fields.links') }}
          </p>
          <FormField v-slot="{ componentField }" name="demo">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.demo') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="github">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.github') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="docs">
            <FormItem>
              <FormLabel>{{ t('career.projects.fields.docs') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="visibility">
          <FormItem>
            <FormLabel>{{ t('career.projects.fields.visibility') }}</FormLabel>
            <FormControl>
              <Select v-bind="componentField">
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectItem value="PRIVATE">
                      {{ t('career.profile.fields.visibility.options.PRIVATE') }}
                    </SelectItem>
                    <SelectItem value="FRIENDS">
                      {{ t('career.profile.fields.visibility.options.FRIENDS') }}
                    </SelectItem>
                    <SelectItem value="PUBLIC">
                      {{ t('career.profile.fields.visibility.options.PUBLIC') }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="space-y-2">
          <Label>{{ t('career.projects.fields.technologies') }}</Label>
          <TechnologyTagInput v-model="technologies" :placeholder="t('career.experiences.fields.technologiesPlaceholder')" />
        </div>

        <div class="space-y-2">
          <Label>{{ t('career.projects.fields.linkedExperiences') }}</Label>
          <div v-if="experiencesQuery.data.value?.length" class="space-y-2 rounded-md border p-3">
            <div
              v-for="experience in experiencesQuery.data.value"
              :key="experience.id"
              class="flex items-center gap-2"
            >
              <Checkbox
                :model-value="experienceIds.includes(experience.id)"
                @update:model-value="toggleExperience(experience.id)"
              />
              <span class="text-sm">{{ experience.position }} &middot; {{ experience.companyName }}</span>
            </div>
          </div>
          <p v-else class="text-sm text-muted-foreground">
            {{ t('career.projects.fields.noExperiences') }}
          </p>
        </div>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            :disabled="saving"
            @click="open = false"
          >
            {{ t('common.cancel') }}
          </Button>
          <Button type="submit" :loading="saving">
            {{ t('career.profile.page.save') }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
