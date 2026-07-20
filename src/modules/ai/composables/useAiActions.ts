/**
 * AI Actions Composable
 * Handles executing actions from AI structured output
 */

import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import type { IAiStructuredOutput } from '../types'

// TODO: structured-output actions (create/update/delete) had a gear-item domain
// wired up before the gear-strip; no domain object exists yet to act on. Rewire
// this to the `career` module's own actions (e.g. update experience/project) once
// it lands. For now this only logs and no-ops.
export function useAiActions() {
  const { t } = useI18n()

  const executeAction = async (
    structuredOutput: IAiStructuredOutput | null,
    _containerId?: string,
  ): Promise<boolean> => {
    if (!structuredOutput || !structuredOutput.action || structuredOutput.action === 'None') {
      return false
    }

    console.warn(`AI action "${structuredOutput.action}" is not wired up to any domain yet`)
    toast.error(t('ai.actions.error'))
    return false
  }

  return {
    executeAction,
  }
}
