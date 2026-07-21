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
import { certificationSchema } from '@/modules/career/validation/certification.schema'
import type { Certification, CreateCertificationData, UpdateCertificationData } from '@/modules/career/types/certification.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  certification?: Certification | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateCertificationData | UpdateCertificationData]
}>()

const isEditing = computed(() => !!props.certification)

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(certificationSchema),
  initialValues: {
    name: '',
    issuingOrganization: '',
    credentialId: '',
    credentialUrl: '',
    issueDate: '',
    expiryDate: '',
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const certification = props.certification
  resetForm({
    values: {
      name: certification?.name ?? '',
      issuingOrganization: certification?.issuingOrganization ?? '',
      credentialId: certification?.credentialId ?? '',
      credentialUrl: certification?.credentialUrl ?? '',
      issueDate: certification?.issueDate ?? '',
      expiryDate: certification?.expiryDate ?? '',
    },
  })
})

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    name: values.name,
    issuingOrganization: values.issuingOrganization,
    credentialId: values.credentialId || null,
    credentialUrl: values.credentialUrl || null,
    issueDate: values.issueDate,
    expiryDate: values.expiryDate || null,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.certifications.form.editTitle') : t('career.certifications.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.certifications.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>{{ t('career.certifications.fields.name') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="issuingOrganization">
          <FormItem>
            <FormLabel>{{ t('career.certifications.fields.issuingOrganization') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="credentialId">
            <FormItem>
              <FormLabel>{{ t('career.certifications.fields.credentialId') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="credentialUrl">
            <FormItem>
              <FormLabel>{{ t('career.certifications.fields.credentialUrl') }}</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="issueDate">
            <FormItem>
              <FormLabel>{{ t('career.certifications.fields.issueDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="expiryDate">
            <FormItem>
              <FormLabel>{{ t('career.certifications.fields.expiryDate') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
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
