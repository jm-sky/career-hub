<script setup lang="ts">
import { Plus, X } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import type { SubProject } from '@/modules/career/types/project.type'

const { t } = useI18n()

const modelValue = defineModel<SubProject[]>({ default: () => [] })

function addRow() {
  modelValue.value = [...modelValue.value, { name: '', url: '' }]
}

function removeRow(index: number) {
  modelValue.value = modelValue.value.filter((_, existing) => existing !== index)
}

function updateRow(index: number, patch: Partial<SubProject>) {
  modelValue.value = modelValue.value.map((row, existing) => existing === index ? { ...row, ...patch } : row)
}
</script>

<template>
  <div class="space-y-2">
    <div
      v-for="(row, index) in modelValue"
      :key="index"
      class="flex items-center gap-2"
    >
      <Input
        :model-value="row.name"
        :placeholder="t('career.projects.fields.subProjectNamePlaceholder')"
        class="flex-1"
        @update:model-value="updateRow(index, { name: String($event) })"
      />
      <Input
        :model-value="row.url ?? ''"
        :placeholder="t('career.projects.fields.subProjectUrlPlaceholder')"
        class="flex-1"
        @update:model-value="updateRow(index, { url: String($event) })"
      />
      <Button
        type="button"
        variant="ghost"
        size="icon"
        @click="removeRow(index)"
      >
        <X class="size-4" />
      </Button>
    </div>
    <Button
      type="button"
      variant="outline"
      size="sm"
      @click="addRow"
    >
      <Plus class="size-4" />
      {{ t('career.projects.fields.addSubProject') }}
    </Button>
  </div>
</template>
