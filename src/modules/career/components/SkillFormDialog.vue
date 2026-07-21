<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { computed, watch } from 'vue'
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
import TechnologyCombobox from '@/modules/career/components/TechnologyCombobox.vue'
import { skillSchema } from '@/modules/career/validation/skill.schema'
import type { CreateSkillData, Skill, UpdateSkillData } from '@/modules/career/types/skill.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  skill?: Skill | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateSkillData | UpdateSkillData]
}>()

const isEditing = computed(() => !!props.skill)

const { handleSubmit, resetForm, values, setFieldValue } = useForm({
  validationSchema: toTypedSchema(skillSchema),
  initialValues: {
    technologyName: '',
    level: 3,
    yearsOfExperience: undefined,
    startedUsingYear: undefined,
    isPrimary: false,
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const skill = props.skill
  resetForm({
    values: {
      technologyName: skill?.technology.name ?? '',
      level: skill?.level ?? 3,
      yearsOfExperience: skill?.yearsOfExperience ?? undefined,
      startedUsingYear: skill?.startedUsingYear ?? undefined,
      isPrimary: skill?.isPrimary ?? false,
    },
  })
})

const onSubmit = handleSubmit((formValues) => {
  emit('submit', {
    technologyName: formValues.technologyName,
    level: formValues.level,
    yearsOfExperience: formValues.yearsOfExperience,
    startedUsingYear: formValues.startedUsingYear,
    isPrimary: formValues.isPrimary,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.skills.form.editTitle') : t('career.skills.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.skills.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <div v-if="!isEditing" class="space-y-2">
          <Label>{{ t('career.skills.fields.technology') }}</Label>
          <TechnologyCombobox
            :model-value="values.technologyName"
            @update:model-value="(value) => setFieldValue('technologyName', value)"
          />
        </div>
        <div v-else class="space-y-2">
          <Label>{{ t('career.skills.fields.technology') }}</Label>
          <p class="text-sm font-medium">
            {{ skill?.technology.name }}
          </p>
        </div>

        <FormField v-slot="{ componentField }" name="level">
          <FormItem>
            <FormLabel>{{ t('career.skills.fields.level') }}</FormLabel>
            <FormControl>
              <Input
                type="number"
                min="1"
                max="5"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="yearsOfExperience">
            <FormItem>
              <FormLabel>{{ t('career.skills.fields.yearsOfExperience') }}</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min="0"
                  step="0.5"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="startedUsingYear">
            <FormItem>
              <FormLabel>{{ t('career.skills.fields.startedUsingYear') }}</FormLabel>
              <FormControl>
                <Input type="number" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="isPrimary">
          <FormItem class="flex items-center gap-2 space-y-0">
            <FormControl>
              <Checkbox
                :model-value="componentField.modelValue"
                @update:model-value="componentField['onUpdate:modelValue']"
              />
            </FormControl>
            <FormLabel class="font-normal">
              {{ t('career.skills.fields.isPrimary') }}
            </FormLabel>
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
