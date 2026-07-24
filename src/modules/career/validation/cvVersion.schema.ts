// modules/career/validation/cvVersion.schema.ts
import { z } from 'zod'

const CV_FONT_FAMILIES = ['sans', 'modern-sans', 'serif', 'minimal-sans', 'mono'] as const
const CV_DENSITIES = ['compact', 'standard', 'spacious'] as const

export const cvVersionSchema = z.object({
  name: z.string().min(1).max(200),
  template: z.string().min(1).max(50),
  accentColor: z.string().regex(/^#[0-9A-Fa-f]{6}$/).optional().or(z.literal('')),
  fontFamily: z.enum(CV_FONT_FAMILIES),
  density: z.enum(CV_DENSITIES),
  customSummary: z.string().optional().or(z.literal('')),
  includePhoto: z.boolean(),
  includeSummary: z.boolean(),
  isDefault: z.boolean(),
})

export type CvVersionFormData = z.infer<typeof cvVersionSchema>
