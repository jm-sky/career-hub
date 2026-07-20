/**
 * AI Context Composable
 * Handles context building for AI requests
 */

import { computed, ref } from 'vue'
import { useAiStore } from '../store/useAiStore'

export interface IAiContext {
  container_ids?: string[]
  fields?: string[]
}

// TODO: `containerIds`/`getContainerData`/`getItemsData` are placeholders left over
// from stripping the gear domain — there's no context data source yet. Rewire this
// to the `career` module's own context (profile/experience/project data) once it lands.
export function useAiContext() {
  const aiStore = useAiStore()

  const selectedContainerIds = ref<string[]>([])
  const selectedFields = ref<string[]>(['name', 'category', 'weight'])

  const availableFields = computed<string[]>(() => {
    // Common fields that can be sent to AI
    return [
      'name',
      'notes',
      'category',
      'weight',
      'quantity',
      'price',
      'url',
      'brand',
      'color',
      'quality',
      'wearable',
      'consumable',
    ]
  })

  const contextFields = computed<string[]>(() => {
    const settingsFields = aiStore.settings?.contextFields
    // Convert Record<string, any> to string[] by taking the keys
    if (settingsFields && typeof settingsFields === 'object' && !Array.isArray(settingsFields)) {
      return Object.keys(settingsFields)
    }
    // Fallback to selectedFields if no settings or if it's already an array (backward compatibility)
    return Array.isArray(settingsFields) ? settingsFields : selectedFields.value
  })

  const buildContext = (): IAiContext => {
    return {
      container_ids: selectedContainerIds.value.length > 0 ? selectedContainerIds.value : undefined,
      fields: selectedFields.value.length > 0 ? selectedFields.value : undefined,
    }
  }

  const getContainerData = (_containerId: string): Record<string, unknown> | undefined => {
    return undefined
  }

  const getItemsData = (_containerId: string): Record<string, unknown>[] => {
    return []
  }

  // No context data source is wired up yet post gear-strip (see TODO above), so this
  // always returns an empty context until the `career` module provides one.
  const buildContextData = (_containerIds?: string[]): Record<string, unknown> => {
    return {}
  }

  const setContainerIds = (ids: string[]): void => {
    selectedContainerIds.value = ids
  }

  const setFields = (fields: string[]): void => {
    selectedFields.value = fields
  }

  const toggleField = (field: string): void => {
    const index = selectedFields.value.indexOf(field)
    if (index > -1) {
      selectedFields.value.splice(index, 1)
    } else {
      selectedFields.value.push(field)
    }
  }

  return {
    selectedContainerIds,
    selectedFields,
    availableFields,
    contextFields,
    buildContext,
    getContainerData,
    getItemsData,
    buildContextData,
    setContainerIds,
    setFields,
    toggleField,
  }
}

