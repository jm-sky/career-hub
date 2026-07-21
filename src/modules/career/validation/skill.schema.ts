// modules/career/validation/skill.schema.ts
import { z } from 'zod'

export const skillSchema = z.object({
  technologyName: z.string().min(1).max(100),
  level: z.coerce.number().min(1).max(5),
  yearsOfExperience: z.coerce.number().min(0).optional(),
  startedUsingYear: z.coerce.number().optional(),
  isPrimary: z.boolean(),
})

export type SkillFormData = z.infer<typeof skillSchema>
