/**
 * TypeScript types for Stripe billing module
 */

export type PlanTier = 'free' | 'pro' | 'expert'

export type BillingInterval = 'monthly' | 'annual'

export type SubscriptionStatus = 'active' | 'canceled' | 'past_due' | 'unpaid' | 'incomplete'

export interface Subscription {
  id: string
  userId: string
  stripeCustomerId: string | null
  stripeSubscriptionId: string | null
  planTier: PlanTier
  billingInterval: BillingInterval | null
  status: SubscriptionStatus
  currentPeriodStart: string | null
  currentPeriodEnd: string | null
  cancelAtPeriodEnd: boolean
  isGrandfathered: boolean
  createdAt: string
  updatedAt: string
}

export interface SubscriptionLimits {
  planTier: PlanTier
  aiMonthlyTokenLimit: number
  storageLimit: number
  canExportData: boolean
  canUseAdvancedFeatures: boolean
  requiresByok: boolean
  cvVersionsLimit: number | null
  pdfWatermark: boolean
  customDomain: boolean
  apiAccess: boolean
}

export interface CreateCheckoutSessionRequest {
  planTier: Exclude<PlanTier, 'free'>
  billingInterval: BillingInterval
  successUrl: string
  cancelUrl: string
}

export interface CheckoutSessionResponse {
  sessionId: string
  sessionUrl: string
}

export interface CreatePortalSessionRequest {
  returnUrl: string
}

export interface PortalSessionResponse {
  sessionUrl: string
}

export interface UpdateOpenRouterTokenRequest {
  openrouterApiToken: string | null
}

export interface PlanFeatures {
  tier: PlanTier
  name: string
  price: {
    monthly: number
    annual: number
    annualMonthly: number // Annual price divided by 12
  }
  features: string[]
  limits: {
    cvVersionsLimit: number | null // null = unlimited
    pdfWatermark: boolean
    aiAccess: boolean
    customDomain: boolean
    apiAccess: boolean
  }
  popular?: boolean
}

export const PLAN_FEATURES: Record<PlanTier, PlanFeatures> = {
  free: {
    tier: 'free',
    name: 'Free',
    price: {
      monthly: 0,
      annual: 0,
      annualMonthly: 0,
    },
    features: [
      'Basic profile management',
      'Data export (JSON/Markdown)',
      'BYOK: Bring Your Own API Key (OpenRouter)',
      '1 CV version',
      'Watermarked PDF export',
    ],
    limits: {
      cvVersionsLimit: 1,
      pdfWatermark: true,
      aiAccess: false,
      customDomain: false,
      apiAccess: false,
    },
  },
  pro: {
    tier: 'pro',
    name: 'Pro',
    price: {
      monthly: 5.0,
      annual: 50,
      annualMonthly: 4.17,
    },
    features: [
      'Everything in Free',
      'AI-powered suggestions',
      '~$1 worth of AI tokens/month',
      'Up to 10 CV versions',
      'No watermark on PDF export',
    ],
    limits: {
      cvVersionsLimit: 10,
      pdfWatermark: false,
      aiAccess: true,
      customDomain: false,
      apiAccess: false,
    },
    popular: true,
  },
  expert: {
    tier: 'expert',
    name: 'Expert',
    price: {
      monthly: 15.0,
      annual: 150,
      annualMonthly: 12.5,
    },
    features: [
      'Everything in Pro',
      'Priority AI processing',
      '~$10 worth of AI tokens/month',
      'Unlimited CV versions',
      'Custom domain for your public profile',
      'API access',
    ],
    limits: {
      cvVersionsLimit: null,
      pdfWatermark: false,
      aiAccess: true,
      customDomain: true,
      apiAccess: true,
    },
  },
}

export const ANNUAL_DISCOUNT_PERCENT = 17
