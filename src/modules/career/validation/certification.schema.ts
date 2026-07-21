// modules/career/validation/certification.schema.ts
import { z } from 'zod'

export const certificationSchema = z.object({
  name: z.string().min(1).max(200),
  issuingOrganization: z.string().min(1).max(200),
  credentialId: z.string().max(100).optional().or(z.literal('')),
  credentialUrl: z.string().max(500).optional().or(z.literal('')),
  issueDate: z.string().min(1),
  expiryDate: z.string().optional().or(z.literal('')),
}).refine(data => !data.expiryDate || data.expiryDate > data.issueDate, {
  message: 'Expiry date must be after issue date.',
  path: ['expiryDate'],
})

export type CertificationFormData = z.infer<typeof certificationSchema>
