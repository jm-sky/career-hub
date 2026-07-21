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
import Select from '@/components/ui/select/Select.vue'
import SelectContent from '@/components/ui/select/SelectContent.vue'
import SelectGroup from '@/components/ui/select/SelectGroup.vue'
import SelectItem from '@/components/ui/select/SelectItem.vue'
import SelectTrigger from '@/components/ui/select/SelectTrigger.vue'
import SelectValue from '@/components/ui/select/SelectValue.vue'
import { Textarea } from '@/components/ui/textarea'
import { languageLevels, languageSchema } from '@/modules/career/validation/language.schema'
import type { CreateLanguageData, Language, UpdateLanguageData } from '@/modules/career/types/language.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  language?: Language | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateLanguageData | UpdateLanguageData]
}>()

const isEditing = computed(() => !!props.language)

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(languageSchema),
  initialValues: {
    name: '',
    level: undefined as undefined | typeof languageLevels[number],
    description: '',
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const language = props.language
  resetForm({
    values: {
      name: language?.name ?? '',
      level: language?.level,
      description: language?.description ?? '',
    },
  })
})

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    name: values.name,
    level: values.level,
    description: values.description || null,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.languages.form.editTitle') : t('career.languages.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.languages.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>{{ t('career.languages.fields.name') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" :placeholder="t('career.languages.fields.namePlaceholder')" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="level">
          <FormItem>
            <FormLabel>{{ t('career.languages.fields.level') }}</FormLabel>
            <FormControl>
              <Select v-bind="componentField">
                <SelectTrigger>
                  <SelectValue :placeholder="t('career.languages.fields.levelPlaceholder')" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectItem
                      v-for="level in languageLevels"
                      :key="level"
                      :value="level"
                    >
                      {{ t(`career.languages.levelOptions.${level}`) }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('career.languages.fields.description') }}</FormLabel>
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
