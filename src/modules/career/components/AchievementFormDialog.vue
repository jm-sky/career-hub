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
import { achievementSchema } from '@/modules/career/validation/achievement.schema'
import type { Achievement, CreateAchievementData, UpdateAchievementData } from '@/modules/career/types/achievement.type'

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

const props = defineProps<{
  achievement?: Achievement | null
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [data: CreateAchievementData | UpdateAchievementData]
}>()

const isEditing = computed(() => !!props.achievement)

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(achievementSchema),
  initialValues: {
    title: '',
    description: '',
    date: '',
    category: undefined,
    url: '',
  },
})

watch(open, (isOpen) => {
  if (!isOpen) return
  const achievement = props.achievement
  resetForm({
    values: {
      title: achievement?.title ?? '',
      description: achievement?.description ?? '',
      date: achievement?.date ?? '',
      category: achievement?.category ?? undefined,
      url: achievement?.url ?? '',
    },
  })
})

const onSubmit = handleSubmit((values) => {
  emit('submit', {
    title: values.title,
    description: values.description || null,
    date: values.date || null,
    category: values.category ?? null,
    url: values.url || null,
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent class="max-h-[90vh] overflow-y-auto sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>
          {{ isEditing ? t('career.achievements.form.editTitle') : t('career.achievements.form.createTitle') }}
        </DialogTitle>
        <DialogDescription>
          {{ t('career.achievements.form.subtitle') }}
        </DialogDescription>
      </DialogHeader>

      <form class="space-y-6" @submit="onSubmit">
        <FormField v-slot="{ componentField }" name="title">
          <FormItem>
            <FormLabel>{{ t('career.achievements.fields.title') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>{{ t('career.achievements.fields.description') }}</FormLabel>
            <FormControl>
              <Textarea v-bind="componentField" rows="3" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="grid gap-6 md:grid-cols-2">
          <FormField v-slot="{ componentField }" name="date">
            <FormItem>
              <FormLabel>{{ t('career.achievements.fields.date') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="category">
            <FormItem>
              <FormLabel>{{ t('career.achievements.fields.category') }}</FormLabel>
              <FormControl>
                <Select v-bind="componentField">
                  <SelectTrigger>
                    <SelectValue :placeholder="t('career.achievements.fields.categoryPlaceholder')" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="AWARD">
                        {{ t('career.achievements.categoryOptions.AWARD') }}
                      </SelectItem>
                      <SelectItem value="PUBLICATION">
                        {{ t('career.achievements.categoryOptions.PUBLICATION') }}
                      </SelectItem>
                      <SelectItem value="SPEAKING">
                        {{ t('career.achievements.categoryOptions.SPEAKING') }}
                      </SelectItem>
                      <SelectItem value="OTHER">
                        {{ t('career.achievements.categoryOptions.OTHER') }}
                      </SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>

        <FormField v-slot="{ componentField }" name="url">
          <FormItem>
            <FormLabel>{{ t('career.achievements.fields.url') }}</FormLabel>
            <FormControl>
              <Input v-bind="componentField" />
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
