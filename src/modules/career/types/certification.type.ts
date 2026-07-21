export interface Certification {
  id: string
  profileId: string
  name: string
  issuingOrganization: string
  credentialId: string | null
  credentialUrl: string | null
  issueDate: string
  expiryDate: string | null
  isExpired: boolean
  displayOrder: number
  createdAt: string
  updatedAt: string
}

export interface CreateCertificationData {
  name: string
  issuingOrganization: string
  credentialId?: string | null
  credentialUrl?: string | null
  issueDate: string
  expiryDate?: string | null
}

export interface UpdateCertificationData {
  name?: string
  issuingOrganization?: string
  credentialId?: string | null
  credentialUrl?: string | null
  issueDate?: string
  expiryDate?: string | null
}

export interface ICertificationService {
  list(): Promise<Certification[]>
  create(data: CreateCertificationData): Promise<Certification>
  update(id: string, data: UpdateCertificationData): Promise<Certification>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Certification[]>
}
