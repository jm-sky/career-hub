// modules/career/validation/achievement.schema.ts
import { z } from 'zod'

export const achievementSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional().or(z.literal('')),
  date: z.string().optional().or(z.literal('')),
  category: z.enum(['AWARD', 'PUBLICATION', 'SPEAKING', 'OTHER']).optional(),
  url: z.string().max(500).optional().or(z.literal('')),
})

export type AchievementFormData = z.infer<typeof achievementSchema>
