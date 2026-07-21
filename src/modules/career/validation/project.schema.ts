// modules/career/validation/project.schema.ts
import { z } from 'zod'

export const projectSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().optional().or(z.literal('')),
  role: z.string().max(200).optional().or(z.literal('')),
  startDate: z.string().min(1),
  endDate: z.string().optional().or(z.literal('')),
  isOngoing: z.boolean(),
  isAnonymized: z.boolean(),
  anonymizedCompany: z.string().max(200).optional().or(z.literal('')),
  status: z.enum(['ACTIVE', 'STAGING', 'ARCHIVED']),
  category: z.enum(['DEMO', 'INTERNAL', 'PRODUCTION']).optional(),
  teamSize: z.coerce.number().min(0).optional(),
  durationMonths: z.coerce.number().min(0).optional(),
  usersCount: z.coerce.number().min(0).optional(),
  budgetRange: z.string().max(50).optional().or(z.literal('')),
  demo: z.string().optional().or(z.literal('')),
  github: z.string().optional().or(z.literal('')),
  docs: z.string().optional().or(z.literal('')),
  visibility: z.enum(['PRIVATE', 'FRIENDS', 'PUBLIC']),
}).refine(data => data.isOngoing || !!data.endDate, {
  message: 'End date is required unless this project is ongoing.',
  path: ['endDate'],
})

export type ProjectFormData = z.infer<typeof projectSchema>
