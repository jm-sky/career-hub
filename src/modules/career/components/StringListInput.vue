<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const { t } = useI18n()

defineProps<{
  placeholder?: string
}>()

const modelValue = defineModel<string[]>({ default: () => [] })

const draft = ref('')

function add() {
  const value = draft.value.trim()
  if (!value) return
  modelValue.value = [...modelValue.value, value]
  draft.value = ''
}

function remove(index: number) {
  modelValue.value = modelValue.value.filter((_, i) => i !== index)
}
</script>

<template>
  <div class="space-y-2">
    <ul v-if="modelValue.length" class="space-y-1">
      <li v-for="(item, index) in modelValue" :key="index" class="flex items-center gap-2 text-sm">
        <span class="flex-1">{{ item }}</span>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          @click="remove(index)"
        >
          {{ t('common.remove') }}
        </Button>
      </li>
    </ul>
    <div class="flex gap-2">
      <Input v-model="draft" :placeholder="placeholder" @keydown.enter.prevent="add" />
      <Button type="button" variant="outline" @click="add">
        {{ t('common.add') }}
      </Button>
    </div>
  </div>
</template>
