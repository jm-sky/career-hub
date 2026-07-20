<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import Button from '@/components/ui/button/Button.vue'

const { t } = useI18n()
const BackIcon = ArrowLeft

defineProps<{
  noLabel?: boolean
}>()
</script>

<template>
  <Button
    variant="ghost"
    size="sm"
  >
    <BackIcon class="size-4" />
    {{ !noLabel ? t('common.back') : null }}
  </Button>
</template>
