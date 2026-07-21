/**
 * Utility functions for translating plan-related content
 */

import type { PlanTier } from '../types'

type TranslateFunction = (key: string, ...args: unknown[]) => string

/**
 * Maps feature strings from PLAN_FEATURES to translation keys
 */
const featureKeyMap: Record<PlanTier, Record<string, string>> = {
  free: {
    'Basic profile management': 'billing.plans.free.features.basicGearManagement',
    'Data export (JSON/Markdown)': 'billing.plans.free.features.dataExport',
    'BYOK: Bring Your Own API Key (OpenRouter)': 'billing.plans.free.features.byok',
    '1 CV version': 'billing.plans.free.features.cvVersionsLimit',
    'Watermarked PDF export': 'billing.plans.free.features.pdfWatermark',
  },
  pro: {
    'Everything in Free': 'billing.plans.pro.features.everythingInFree',
    'AI-powered suggestions': 'billing.plans.pro.features.aiRecommendations',
    '~$1 worth of AI tokens/month': 'billing.plans.pro.features.aiTokens',
    'Up to 10 CV versions': 'billing.plans.pro.features.cvVersionsLimit',
    'No watermark on PDF export': 'billing.plans.pro.features.pdfWatermark',
  },
  expert: {
    'Everything in Pro': 'billing.plans.expert.features.everythingInPro',
    'Priority AI processing': 'billing.plans.expert.features.priorityAi',
    '~$10 worth of AI tokens/month': 'billing.plans.expert.features.aiTokens',
    'Unlimited CV versions': 'billing.plans.expert.features.cvVersionsLimit',
    'Custom domain for your public profile': 'billing.plans.expert.features.customDomain',
    'API access': 'billing.plans.expert.features.apiAccess',
  },
}

/**
 * Get translated features for a plan tier
 */
export function getTranslatedFeatures(
  planTier: PlanTier,
  features: string[],
  t: TranslateFunction,
): string[] {
  const keyMap = featureKeyMap[planTier]
  
  return features.map((feature) => {
    const translationKey = keyMap[feature]
    return translationKey ? t(translationKey) : feature
  })
}

/**
 * Get translated plan name with suffix
 */
export function getTranslatedPlanName(planTier: PlanTier, t: TranslateFunction): string {
  const planKey = `billing.plans.${planTier}.fullName` as const
  return t(planKey)
}

