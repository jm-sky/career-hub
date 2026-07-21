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
import { Textarea } from '@/components/ui/textarea'
import TechnologyTagInput from '@/modules/career/components/TechnologyTagInput.vue'
import { experienceSchema } from '@/modules/career/validation/experience.schema'
import type { CreateExperienceData, Experience, UpdateExperienceData } from '@/modules/career/types/experience.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  experience?: Experience | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateExperienceData | UpdateExperienceData]
}>()

const isEditing = computed(() => !!props.experience)

const responsibilities = ref<string[]>([])
const responsibilityDraft = ref('')
const technologies = ref<string[]>([])

const { handleSubmit, resetForm, values } = useForm({
  validationSchema: toTypedSchema(experienceSchema),
  initialValues: {
    companyName: '',
    position: '',
    employmentType: '',
    startDate: '',
    endDate: '',
    isCurrent: false,
    description: '',
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const experience = props.experience
  resetForm({
    values: {
      companyName: experience?.companyName ?? '',
      position: experience?.position ?? '',
      employmentType: experience?.employmentType ?? '',
      startDate: experience?.startDate ?? '',
      endDate: experience?.endDate ?? '',
      isCurrent: experience?.isCurrent ?? false,
      description: experience?.description ?? '',
    },
  })
  responsibilities.value = experience?.responsibilities ? [...experience.responsibilities] : []
  technologies.value = experience?.technologies ? experience.technologies.map(technology => technology.name) : []
  responsibilityDraft.value = ''
})

function addResponsibility() {
  const value = responsibilityDraft.value.trim()
  if (!value) return
  responsibilities.value = [...responsibilities.value, value]
  responsibilityDraft.value = ''
}

function removeResponsibility(index: number) {
  responsibilities.value = responsibilities.value.filter((_, i) => i !== index)
}

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    companyName: values.companyName,
    position: values.position,
    employmentType: values.employmentType || null,
    startDate: values.startDate,
    endDate: values.isCurrent ? null : (values.endDate || null),
    isCurrent: values.isCurrent,
    description: values.description || null,
    responsibilities: responsibilities.value,
    technologies: technologies.value,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.experiences.form.editTitle') : t('career.experiences.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.experiences.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="companyName">
            <FormItem>
              <FormLabel>{{ t('career.experiences.fields.companyName') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="position">
            <FormItem>
              <FormLabel>{{ t('career.experiences.fields.position') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="employmentType">
          <FormItem>
            <FormLabel>{{ t('career.experiences.fields.employmentType') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" :placeholder="t('career.experiences.fields.employmentTypePlaceholder')" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="startDate">
            <FormItem>
              <FormLabel>{{ t('career.experiences.fields.startDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="endDate">
            <FormItem>
              <FormLabel>{{ t('career.experiences.fields.endDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" :disabled="values.isCurrent" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="isCurrent">
          <FormItem class="flex items-center gap-2 space-y-0">
            <FormControl>
              <Checkbox v-bind="componentField" />
            </FormControl>
            <FormLabel class="font-normal">
              {{ t('career.experiences.fields.isCurrent') }}
            </FormLabel>
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('career.experiences.fields.description') }}</FormLabel>
            <FormControl>
              <Textarea v-bind="componentField" rows="3" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.experiences.fields.responsibilities') }}
          </p>
          <ul v-if="responsibilities.length" class="space-y-1">
            <li v-for="(item, index) in responsibilities" :key="index" class="flex items-center gap-2 text-sm">
              <span class="flex-1">{{ item }}</span>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                @click="removeResponsibility(index)"
              >
                {{ t('common.remove') }}
              </Button>
            </li>
          </ul>
          <div class="flex gap-2">
            <Input
              v-model="responsibilityDraft"
              :placeholder="t('career.experiences.fields.responsibilitiesPlaceholder')"
              @keydown.enter.prevent="addResponsibility"
            />
            <Button type="button" variant="outline" @click="addResponsibility">
              {{ t('common.add') }}
            </Button>
          </div>
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium">
            {{ t('career.experiences.fields.technologies') }}
          </p>
          <TechnologyTagInput v-model="technologies" :placeholder="t('career.experiences.fields.technologiesPlaceholder')" />
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
