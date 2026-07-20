// modules/career/validation/profile.schema.ts
import { z } from 'zod'

export const profileSchema = z.object({
  headline: z.string().max(200).optional().or(z.literal('')),
  summary: z.string().optional().or(z.literal('')),
  location: z.string().max(120).optional().or(z.literal('')),
  visibility: z.enum(['PRIVATE', 'FRIENDS', 'PUBLIC']),
  email: z.string().email().optional().or(z.literal('')),
  phone: z.string().optional().or(z.literal('')),
  linkedin: z.string().optional().or(z.literal('')),
  website: z.string().optional().or(z.literal('')),
})

export type ProfileFormData = z.infer<typeof profileSchema>
