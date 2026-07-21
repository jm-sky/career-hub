<script setup lang="ts">
import { XIcon } from 'lucide-vue-next'
import { ref, watch } from 'vue'
import { Badge } from '@/components/ui/badge'
import TechnologyCombobox from '@/modules/career/components/TechnologyCombobox.vue'

defineProps<{
  placeholder?: string
}>()

const modelValue = defineModel<string[]>({ default: () => [] })

const pendingValue = ref('')

watch(pendingValue, (name) => {
  if (!name) return
  const exists = modelValue.value.some(existing => existing.toLowerCase() === name.toLowerCase())
  if (!exists) modelValue.value = [...modelValue.value, name]
  pendingValue.value = ''
})

function remove(name: string) {
  modelValue.value = modelValue.value.filter(existing => existing !== name)
}
</script>

<template>
  <div class="space-y-2">
    <div v-if="modelValue.length" class="flex flex-wrap gap-2">
      <Badge
        v-for="name in modelValue"
        :key="name"
        variant="secondary"
        class="gap-1"
      >
        {{ name }}
        <button type="button" class="cursor-pointer" @click="remove(name)">
          <XIcon class="size-3" />
        </button>
      </Badge>
    </div>
    <TechnologyCombobox v-model="pendingValue" :placeholder="placeholder" />
  </div>
</template>
