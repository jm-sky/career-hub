<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
  as?: string
}>()
</script>

<template>
  <component
    :is="as ?? 'div'"
    data-slot="card"
    :class="
      cn(
        'bg-card text-card-foreground flex flex-col gap-6 rounded-xl border border-border py-6 shadow-sm',
        'transition-[transform,box-shadow,border-color,translate] duration-300 ease-out hover:-translate-y-1 hover:border-primary/25 hover:shadow-lg hover:shadow-primary/10 motion-reduce:transition-none motion-reduce:hover:translate-y-0',
        props.class,
      )
    "
  >
    <slot />
  </component>
</template>
