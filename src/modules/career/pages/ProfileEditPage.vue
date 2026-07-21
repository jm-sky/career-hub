<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { UserRound } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import { watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import Select from '@/components/ui/select/Select.vue'
import SelectContent from '@/components/ui/select/SelectContent.vue'
import SelectGroup from '@/components/ui/select/SelectGroup.vue'
import SelectItem from '@/components/ui/select/SelectItem.vue'
import SelectTrigger from '@/components/ui/select/SelectTrigger.vue'
import SelectValue from '@/components/ui/select/SelectValue.vue'
import Separator from '@/components/ui/separator/Separator.vue'
import { Textarea } from '@/components/ui/textarea'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'
import { publicProfilePath } from '@/modules/career/routes'
import { profileSchema } from '@/modules/career/validation/profile.schema'
import { useProfile } from '../composables/useProfile'
import type { Profile } from '@/modules/career/types/profile.type'

const { t } = useI18n()
const { profileQuery, profile, updateProfile, isLoading, isUpdating, isError } = useProfile()

const { handleSubmit, setValues } = useForm({
  validationSchema: toTypedSchema(profileSchema),
  initialValues: {
    headline: profile.value?.headline ?? '',
    summary: profile.value?.summary ?? '',
    location: profile.value?.location ?? '',
    visibility: profile.value?.visibility ?? 'PRIVATE',
    email: profile.value?.contact?.email ?? '',
    phone: profile.value?.contact?.phone ?? '',
    linkedin: profile.value?.contact?.linkedin ?? '',
    website: profile.value?.contact?.website ?? '',
  },
})

watch(() => profileQuery.data.value, (val: Profile | undefined) => {
  if (val) {
    setValues({
      headline: val.headline ?? '',
      summary: val.summary ?? '',
      location: val.location ?? '',
      visibility: val.visibility,
      email: val.contact?.email ?? '',
      phone: val.contact?.phone ?? '',
      linkedin: val.contact?.linkedin ?? '',
      website: val.contact?.website ?? '',
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  try {
    await updateProfile({
      headline: values.headline || null,
      summary: values.summary || null,
      location: values.location || null,
      visibility: values.visibility,
      contact: {
        email: values.email || null,
        phone: values.phone || null,
        linkedin: values.linkedin || null,
        website: values.website || null,
      },
    })
    toast.success(t('common.copyToClipboard.success', 'Saved'))
  } catch {
    toast.error(t('errors.generic'))
  }
})
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-6">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold tracking-tight">
          {{ t('career.profile.page.title') }}
        </h1>
        <p class="text-muted-foreground">
          {{ t('career.profile.page.subtitle') }}
        </p>
        <p v-if="profile" class="text-sm text-muted-foreground">
          {{ t('career.profile.page.completeness', { score: profile.completenessScore }) }}
          &middot;
          <RouterLink :to="publicProfilePath(profile.slug)" class="text-primary hover:underline">
            {{ publicProfilePath(profile.slug) }}
          </RouterLink>
        </p>
      </div>

      <Card>
        <CardHeader>
          <div class="flex items-center gap-2">
            <UserRound :size="20" />
            <CardTitle>{{ t('career.profile.page.title') }}</CardTitle>
          </div>
          <CardDescription>{{ t('career.profile.page.subtitle') }}</CardDescription>
        </CardHeader>
        <CardContent :class="{ 'opacity-50': isUpdating }">
          <div v-if="isLoading" class="space-y-4">
            <div class="h-16 bg-muted rounded animate-pulse" />
            <div class="h-16 bg-muted rounded animate-pulse" />
          </div>

          <div v-else-if="isError" class="bg-destructive/10 border border-destructive/20 text-destructive rounded-lg p-4">
            {{ t('career.profile.page.error_prefix') }}
          </div>

          <form v-else class="space-y-6" @submit="onSubmit">
            <FormField v-slot="{ componentField }" name="headline">
              <FormItem>
                <FormLabel>{{ t('career.profile.fields.headline.label') }}</FormLabel>
                <FormControl>
                  <Input v-bind="componentField" :placeholder="t('career.profile.fields.headline.placeholder')" />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="summary">
              <FormItem>
                <FormLabel>{{ t('career.profile.fields.summary.label') }}</FormLabel>
                <FormControl>
                  <Textarea v-bind="componentField" rows="4" :placeholder="t('career.profile.fields.summary.placeholder')" />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <div class="grid gap-6 md:grid-cols-2">
              <FormField v-slot="{ componentField }" name="location">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.location.label') }}</FormLabel>
                  <FormControl>
                    <Input v-bind="componentField" :placeholder="t('career.profile.fields.location.placeholder')" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="visibility">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.visibility.label') }}</FormLabel>
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
            </div>

            <Separator />

            <div class="space-y-1">
              <h3 class="text-sm font-semibold">
                {{ t('career.profile.fields.contact.title') }}
              </h3>
              <p class="text-sm text-muted-foreground">
                {{ t('career.profile.fields.contact.subtitle') }}
              </p>
            </div>

            <div class="grid gap-6 md:grid-cols-2">
              <FormField v-slot="{ componentField }" name="email">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.contact.email') }}</FormLabel>
                  <FormControl>
                    <Input type="email" v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="phone">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.contact.phone') }}</FormLabel>
                  <FormControl>
                    <Input v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="linkedin">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.contact.linkedin') }}</FormLabel>
                  <FormControl>
                    <Input v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="website">
                <FormItem>
                  <FormLabel>{{ t('career.profile.fields.contact.website') }}</FormLabel>
                  <FormControl>
                    <Input v-bind="componentField" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>
            </div>

            <div class="flex justify-end">
              <Button type="submit" :loading="isUpdating">
                {{ t('career.profile.page.save') }}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </AuthenticatedLayout>
</template>
