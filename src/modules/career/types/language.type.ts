export type LanguageLevel = 'NATIVE' | 'C2' | 'C1' | 'B2' | 'B1' | 'A2' | 'A1'

export interface Language {
  id: string
  profileId: string
  name: string
  level: LanguageLevel
  description: string | null
  displayOrder: number
  createdAt: string
  updatedAt: string
}

export interface CreateLanguageData {
  name: string
  level: LanguageLevel
  description?: string | null
}

export interface UpdateLanguageData {
  name?: string
  level?: LanguageLevel
  description?: string | null
}

export interface ILanguageService {
  list(): Promise<Language[]>
  create(data: CreateLanguageData): Promise<Language>
  update(id: string, data: UpdateLanguageData): Promise<Language>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Language[]>
}
