<script setup lang="ts">
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

const { t } = useI18n()

const open = defineModel<boolean>('open', { required: true })

defineProps<{
  title: string
  description: string
  loading?: boolean
}>()

const emit = defineEmits<{
  confirm: []
}>()
</script>

<template>
  <Dialog :open="open" @update:open="(value) => { open = value }">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ title }}</DialogTitle>
        <DialogDescription>{{ description }}</DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button variant="outline" :disabled="loading" @click="open = false">
          {{ t('common.cancel') }}
        </Button>
        <Button
          variant="destructive"
          :disabled="loading"
          :loading="loading"
          @click="emit('confirm')"
        >
          {{ t('common.delete') }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
