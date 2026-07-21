<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
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
import { educationSchema } from '@/modules/career/validation/education.schema'
import type { CreateEducationData, Education, UpdateEducationData } from '@/modules/career/types/education.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  education?: Education | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateEducationData | UpdateEducationData]
}>()

const isEditing = computed(() => !!props.education)

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(educationSchema),
  initialValues: {
    institution: '',
    degree: '',
    fieldOfStudy: '',
    startDate: '',
    endDate: '',
    grade: '',
    description: '',
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const education = props.education
  resetForm({
    values: {
      institution: education?.institution ?? '',
      degree: education?.degree ?? '',
      fieldOfStudy: education?.fieldOfStudy ?? '',
      startDate: education?.startDate ?? '',
      endDate: education?.endDate ?? '',
      grade: education?.grade ?? '',
      description: education?.description ?? '',
    },
  })
})

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    institution: values.institution,
    degree: values.degree,
    fieldOfStudy: values.fieldOfStudy || null,
    startDate: values.startDate,
    endDate: values.endDate || null,
    grade: values.grade || null,
    description: values.description || null,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.education.form.editTitle') : t('career.education.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.education.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="institution">
          <FormItem>
            <FormLabel>{{ t('career.education.fields.institution') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="degree">
            <FormItem>
              <FormLabel>{{ t('career.education.fields.degree') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="fieldOfStudy">
            <FormItem>
              <FormLabel>{{ t('career.education.fields.fieldOfStudy') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="startDate">
            <FormItem>
              <FormLabel>{{ t('career.education.fields.startDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="endDate">
            <FormItem>
              <FormLabel>{{ t('career.education.fields.endDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="grade">
          <FormItem>
            <FormLabel>{{ t('career.education.fields.grade') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" :placeholder="t('career.education.fields.gradePlaceholder')" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('career.education.fields.description') }}</FormLabel>
            <FormControl>
              <Textarea v-bind="componentField" rows="3" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

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
