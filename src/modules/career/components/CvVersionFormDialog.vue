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
import Select from '@/components/ui/select/Select.vue'
import SelectContent from '@/components/ui/select/SelectContent.vue'
import SelectGroup from '@/components/ui/select/SelectGroup.vue'
import SelectItem from '@/components/ui/select/SelectItem.vue'
import SelectTrigger from '@/components/ui/select/SelectTrigger.vue'
import SelectValue from '@/components/ui/select/SelectValue.vue'
import { Textarea } from '@/components/ui/textarea'
import SectionIdPicker from '@/modules/career/components/SectionIdPicker.vue'
import { useAchievementsQuery } from '@/modules/career/composables/useAchievements'
import { useCertificationsQuery } from '@/modules/career/composables/useCertifications'
import { useEducationQuery } from '@/modules/career/composables/useEducation'
import { useExperiencesQuery } from '@/modules/career/composables/useExperiences'
import { useLanguagesQuery } from '@/modules/career/composables/useLanguages'
import { useProjectsQuery } from '@/modules/career/composables/useProjects'
import { useSkillsQuery } from '@/modules/career/composables/useSkills'
import { cvVersionSchema } from '@/modules/career/validation/cvVersion.schema'
import type { CreateCvVersionData, CvVersion, UpdateCvVersionData } from '@/modules/career/types/cvVersion.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  cvVersion?: CvVersion | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateCvVersionData | UpdateCvVersionData]
}>()

const isEditing = computed(() => !!props.cvVersion)

const experienceIds = ref<string[]>([])
const projectIds = ref<string[]>([])
const skillIds = ref<string[]>([])
const educationIds = ref<string[]>([])
const certificationIds = ref<string[]>([])
const achievementIds = ref<string[]>([])
const languageIds = ref<string[]>([])

const experiencesQuery = useExperiencesQuery()
const projectsQuery = useProjectsQuery()
const skillsQuery = useSkillsQuery()
const educationQuery = useEducationQuery()
const certificationsQuery = useCertificationsQuery()
const achievementsQuery = useAchievementsQuery()
const languagesQuery = useLanguagesQuery()

const experienceItems = computed(() => (experiencesQuery.data.value ?? []).map(e => ({ id: e.id, label: `${e.position} · ${e.companyName}` })))
const projectItems = computed(() => (projectsQuery.data.value ?? []).map(p => ({ id: p.id, label: p.name })))
const skillItems = computed(() => (skillsQuery.data.value ?? []).map(s => ({ id: s.id, label: s.technology.name })))
const educationItems = computed(() => (educationQuery.data.value ?? []).map(e => ({ id: e.id, label: `${e.degree} · ${e.institution}` })))
const certificationItems = computed(() => (certificationsQuery.data.value ?? []).map(c => ({ id: c.id, label: c.name })))
const achievementItems = computed(() => (achievementsQuery.data.value ?? []).map(a => ({ id: a.id, label: a.title })))
const languageItems = computed(() => (languagesQuery.data.value ?? []).map(l => ({ id: l.id, label: `${l.name} · ${l.level}` })))

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(cvVersionSchema),
  initialValues: {
    name: '',
    template: 'default',
    customSummary: '',
    includePhoto: true,
    includeSummary: true,
    isDefault: false,
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const cv = props.cvVersion
  resetForm({
    values: {
      name: cv?.name ?? '',
      template: cv?.template ?? 'default',
      customSummary: cv?.sectionsConfig.customSummary ?? '',
      includePhoto: cv?.sectionsConfig.includePhoto ?? true,
      includeSummary: cv?.sectionsConfig.includeSummary ?? true,
      isDefault: cv?.isDefault ?? false,
    },
  })
  experienceIds.value = cv?.sectionsConfig.experienceIds ? [...cv.sectionsConfig.experienceIds] : []
  projectIds.value = cv?.sectionsConfig.projectIds ? [...cv.sectionsConfig.projectIds] : []
  skillIds.value = cv?.sectionsConfig.skillIds ? [...cv.sectionsConfig.skillIds] : []
  educationIds.value = cv?.sectionsConfig.educationIds ? [...cv.sectionsConfig.educationIds] : []
  certificationIds.value = cv?.sectionsConfig.certificationIds ? [...cv.sectionsConfig.certificationIds] : []
  achievementIds.value = cv?.sectionsConfig.achievementIds ? [...cv.sectionsConfig.achievementIds] : []
  languageIds.value = cv?.sectionsConfig.languageIds ? [...cv.sectionsConfig.languageIds] : []
})

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    name: values.name,
    template: values.template,
    isDefault: values.isDefault,
    sectionsConfig: {
      experienceIds: experienceIds.value,
      projectIds: projectIds.value,
      skillIds: skillIds.value,
      educationIds: educationIds.value,
      certificationIds: certificationIds.value,
      achievementIds: achievementIds.value,
      languageIds: languageIds.value,
      customSummary: values.customSummary || null,
      includePhoto: values.includePhoto,
      includeSummary: values.includeSummary,
    },
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.cvVersions.form.editTitle') : t('career.cvVersions.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.cvVersions.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="name">
            <FormItem>
              <FormLabel>{{ t('career.cvVersions.fields.name') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="template">
            <FormItem>
              <FormLabel>{{ t('career.cvVersions.fields.template') }}</FormLabel>
              <FormControl>
                <Select v-bind="componentField">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="default">
                        {{ t('career.cvVersions.templateOptions.default') }}
                      </SelectItem>
                      <SelectItem value="modern">
                        {{ t('career.cvVersions.templateOptions.modern') }}
                      </SelectItem>
                      <SelectItem value="classic">
                        {{ t('career.cvVersions.templateOptions.classic') }}
                      </SelectItem>
                      <SelectItem value="minimal">
                        {{ t('career.cvVersions.templateOptions.minimal') }}
                      </SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="customSummary">
          <FormItem>
            <FormLabel>{{ t('career.cvVersions.fields.customSummary') }}</FormLabel>
            <FormControl>
              <Textarea v-bind="componentField" rows="3" :placeholder="t('career.cvVersions.fields.customSummaryPlaceholder')" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="flex flex-wrap gap-6">
          <FormField v-slot="{ componentField }" name="includeSummary">
            <FormItem class="flex items-center gap-2 space-y-0">
              <FormControl>
                <Checkbox
                  :model-value="componentField.modelValue"
                  @update:model-value="componentField['onUpdate:modelValue']"
                />
              </FormControl>
              <FormLabel class="font-normal">
                {{ t('career.cvVersions.fields.includeSummary') }}
              </FormLabel>
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="includePhoto">
            <FormItem class="flex items-center gap-2 space-y-0">
              <FormControl>
                <Checkbox
                  :model-value="componentField.modelValue"
                  @update:model-value="componentField['onUpdate:modelValue']"
                />
              </FormControl>
              <FormLabel class="font-normal">
                {{ t('career.cvVersions.fields.includePhoto') }}
              </FormLabel>
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="isDefault">
            <FormItem class="flex items-center gap-2 space-y-0">
              <FormControl>
                <Checkbox
                  :model-value="componentField.modelValue"
                  @update:model-value="componentField['onUpdate:modelValue']"
                />
              </FormControl>
              <FormLabel class="font-normal">
                {{ t('career.cvVersions.fields.isDefault') }}
              </FormLabel>
            </FormItem>
          </FormField>
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.experiences') }}
          </p>
          <SectionIdPicker v-model="experienceIds" :items="experienceItems" :empty-message="t('career.cvVersions.fields.noExperiences')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.projects') }}
          </p>
          <SectionIdPicker v-model="projectIds" :items="projectItems" :empty-message="t('career.cvVersions.fields.noProjects')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.skills') }}
          </p>
          <SectionIdPicker v-model="skillIds" :items="skillItems" :empty-message="t('career.cvVersions.fields.noSkills')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.education') }}
          </p>
          <SectionIdPicker v-model="educationIds" :items="educationItems" :empty-message="t('career.cvVersions.fields.noEducation')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.certifications') }}
          </p>
          <SectionIdPicker v-model="certificationIds" :items="certificationItems" :empty-message="t('career.cvVersions.fields.noCertifications')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.achievements') }}
          </p>
          <SectionIdPicker v-model="achievementIds" :items="achievementItems" :empty-message="t('career.cvVersions.fields.noAchievements')" />
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.cvVersions.fields.languages') }}
          </p>
          <SectionIdPicker v-model="languageIds" :items="languageItems" :empty-message="t('career.cvVersions.fields.noLanguages')" />
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
