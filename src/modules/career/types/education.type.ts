export interface Education {
  id: string
  profileId: string
  institution: string
  degree: string
  fieldOfStudy: string | null
  startDate: string
  endDate: string | null
  grade: string | null
  description: string | null
  displayOrder: number
  createdAt: string
  updatedAt: string
}

export interface CreateEducationData {
  institution: string
  degree: string
  fieldOfStudy?: string | null
  startDate: string
  endDate?: string | null
  grade?: string | null
  description?: string | null
}

export interface UpdateEducationData {
  institution?: string
  degree?: string
  fieldOfStudy?: string | null
  startDate?: string
  endDate?: string | null
  grade?: string | null
  description?: string | null
}

export interface IEducationService {
  list(): Promise<Education[]>
  create(data: CreateEducationData): Promise<Education>
  update(id: string, data: UpdateEducationData): Promise<Education>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Education[]>
}
