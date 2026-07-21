import { z } from 'zod'

export const languageLevels = ['NATIVE', 'C2', 'C1', 'B2', 'B1', 'A2', 'A1'] as const

export const languageSchema = z.object({
  name: z.string().min(1).max(100),
  level: z.enum(languageLevels),
  description: z.string().optional().or(z.literal('')),
})

export type LanguageFormData = z.infer<typeof languageSchema>
