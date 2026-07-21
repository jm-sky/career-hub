// modules/career/validation/experience.schema.ts
import { z } from 'zod'

export const experienceSchema = z.object({
  companyName: z.string().min(1).max(200),
  position: z.string().min(1).max(200),
  employmentType: z.string().max(30).optional().or(z.literal('')),
  startDate: z.string().min(1),
  endDate: z.string().optional().or(z.literal('')),
  isCurrent: z.boolean(),
  description: z.string().optional().or(z.literal('')),
}).refine(data => data.isCurrent || !!data.endDate, {
  message: 'End date is required unless this is your current role.',
  path: ['endDate'],
})

export type ExperienceFormData = z.infer<typeof experienceSchema>
