<script setup lang="ts">
import { cn } from '@/lib/utils'
import { config } from '@/shared/config/config'
import type { PrimitiveProps } from 'reka-ui'
import type { HTMLAttributes } from 'vue'

const props = withDefaults(defineProps<{
  as?: PrimitiveProps['as']
  class?: HTMLAttributes['class']
}>(), {
  as: 'span',
})
</script>

<template>
  <component :is="props.as" :class="cn('bg-linear-to-r from-primary via-warm to-primary bg-clip-text text-2xl font-bold text-transparent', props.class)">
    {{ config.app.name }}
  </component>
</template>
