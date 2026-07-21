<script setup lang="ts">
import { Checkbox } from '@/components/ui/checkbox'

defineProps<{
  items: { id: string, label: string }[]
  emptyMessage: string
}>()

const modelValue = defineModel<string[]>({ default: () => [] })

function toggle(id: string) {
  modelValue.value = modelValue.value.includes(id)
    ? modelValue.value.filter(existing => existing !== id)
    : [...modelValue.value, id]
}
</script>

<template>
  <div v-if="items.length" class="max-h-48 space-y-2 overflow-y-auto rounded-md border p-3">
    <button
      v-for="item in items"
      :key="item.id"
      type="button"
      class="flex w-full items-center gap-2 text-left"
      @click="toggle(item.id)"
    >
      <Checkbox :model-value="modelValue.includes(item.id)" class="pointer-events-none" />
      <span class="text-sm">{{ item.label }}</span>
    </button>
  </div>
  <p v-else class="text-sm text-muted-foreground">
    {{ emptyMessage }}
  </p>
</template>
