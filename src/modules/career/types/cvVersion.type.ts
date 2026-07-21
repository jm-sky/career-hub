export interface CvSectionsConfig {
  experienceIds: string[]
  projectIds: string[]
  skillIds: string[]
  educationIds: string[]
  certificationIds: string[]
  achievementIds: string[]
  languageIds: string[]
  customSummary: string | null
  includePhoto: boolean
  includeSummary: boolean
}

export interface CvVersion {
  id: string
  profileId: string
  name: string
  template: string
  sectionsConfig: CvSectionsConfig
  pdfUrl: string | null
  isDefault: boolean
  createdAt: string
  updatedAt: string
}

export interface CreateCvVersionData {
  name: string
  template?: string
  sectionsConfig?: Partial<CvSectionsConfig>
  isDefault?: boolean
}

export interface UpdateCvVersionData {
  name?: string
  template?: string
  sectionsConfig?: Partial<CvSectionsConfig>
  isDefault?: boolean
}

export type GenerateCvVersionStatus = 'queued'

export interface GenerateCvVersionResult {
  jobId: string
  status: GenerateCvVersionStatus
}

export interface ICvVersionService {
  list(): Promise<CvVersion[]>
  create(data: CreateCvVersionData): Promise<CvVersion>
  update(id: string, data: UpdateCvVersionData): Promise<CvVersion>
  delete(id: string): Promise<void>
  generate(id: string): Promise<GenerateCvVersionResult>
  getDownloadUrl(id: string): Promise<string>
}
