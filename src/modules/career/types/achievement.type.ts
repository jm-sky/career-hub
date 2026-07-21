export type AchievementCategory = 'AWARD' | 'PUBLICATION' | 'SPEAKING' | 'OTHER'

export interface Achievement {
  id: string
  profileId: string
  title: string
  description: string | null
  date: string | null
  category: AchievementCategory | null
  url: string | null
  displayOrder: number
  createdAt: string
  updatedAt: string
}

export interface CreateAchievementData {
  title: string
  description?: string | null
  date?: string | null
  category?: AchievementCategory | null
  url?: string | null
}

export interface UpdateAchievementData {
  title?: string
  description?: string | null
  date?: string | null
  category?: AchievementCategory | null
  url?: string | null
}

export interface IAchievementService {
  list(): Promise<Achievement[]>
  create(data: CreateAchievementData): Promise<Achievement>
  update(id: string, data: UpdateAchievementData): Promise<Achievement>
  delete(id: string): Promise<void>
  reorder(orderedIds: string[]): Promise<Achievement[]>
}
