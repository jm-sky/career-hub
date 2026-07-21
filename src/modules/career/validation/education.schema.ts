// modules/career/validation/education.schema.ts
import { z } from 'zod'

export const educationSchema = z.object({
  institution: z.string().min(1).max(200),
  degree: z.string().min(1).max(200),
  fieldOfStudy: z.string().max(200).optional().or(z.literal('')),
  startDate: z.string().min(1),
  endDate: z.string().optional().or(z.literal('')),
  grade: z.string().max(50).optional().or(z.literal('')),
  description: z.string().optional().or(z.literal('')),
}).refine(data => !data.endDate || data.endDate > data.startDate, {
  message: 'End date must be after start date.',
  path: ['endDate'],
})

export type EducationFormData = z.infer<typeof educationSchema>
