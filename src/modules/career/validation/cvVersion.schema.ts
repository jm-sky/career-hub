// modules/career/validation/cvVersion.schema.ts
import { z } from 'zod'

export const cvVersionSchema = z.object({
  name: z.string().min(1).max(200),
  template: z.string().min(1).max(50),
  accentColor: z.string().regex(/^#[0-9A-Fa-f]{6}$/).optional().or(z.literal('')),
  customSummary: z.string().optional().or(z.literal('')),
  includePhoto: z.boolean(),
  includeSummary: z.boolean(),
  isDefault: z.boolean(),
})

export type CvVersionFormData = z.infer<typeof cvVersionSchema>
