<script setup lang="ts">
import { computed, ref } from 'vue'
import ComboBox from '@/components/ui/combo-box/ComboBox.vue'
import { useTechnologySearch } from '@/modules/career/composables/useTechnologies'
import type { ComboBoxOption } from '@/components/ui/combo-box/ComboBox.vue'

defineProps<{
  placeholder?: string
}>()

const modelValue = defineModel<string>({ default: '' })

const { data: technologies } = useTechnologySearch(ref(undefined))

const options = computed<ComboBoxOption[]>(() =>
  (technologies.value ?? []).map(technology => ({ value: technology.name, label: technology.name })),
)
</script>

<template>
  <ComboBox
    v-model:value="modelValue"
    :options="options"
    :placeholder="placeholder"
    creatable
    clearable
  />
</template>
