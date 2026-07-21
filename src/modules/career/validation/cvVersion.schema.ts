// modules/career/validation/cvVersion.schema.ts
import { z } from 'zod'

export const cvVersionSchema = z.object({
  name: z.string().min(1).max(200),
  template: z.string().min(1).max(50),
  customSummary: z.string().optional().or(z.literal('')),
  includePhoto: z.boolean(),
  includeSummary: z.boolean(),
  isDefault: z.boolean(),
})

export type CvVersionFormData = z.infer<typeof cvVersionSchema>
