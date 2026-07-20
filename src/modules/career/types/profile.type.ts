export type ProfileVisibility = 'PRIVATE' | 'FRIENDS' | 'PUBLIC'

export interface ContactInfo {
  email?: string | null
  phone?: string | null
  linkedin?: string | null
  website?: string | null
}

export interface Profile {
  id: string
  userId: string
  slug: string
  headline: string | null
  summary: string | null
  location: string | null
  visibility: ProfileVisibility
  contact: ContactInfo
  draftData: Record<string, unknown>
  profilePhotoUrl: string | null
  completenessScore: number
  createdAt: string
  updatedAt: string
}

export interface PublicProfile {
  slug: string
  headline: string | null
  summary: string | null
  location: string | null
  profilePhotoUrl: string | null
}

export interface UpdateProfileData {
  headline?: string | null
  summary?: string | null
  location?: string | null
  visibility?: ProfileVisibility
  contact?: ContactInfo
  profilePhotoUrl?: string | null
  slug?: string
}

export interface ProfileDraftData {
  step: string
  data: Record<string, unknown>
}

export interface IProfileService {
  getMyProfile(): Promise<Profile>
  updateMyProfile(data: UpdateProfileData): Promise<Profile>
  saveDraft(draft: ProfileDraftData): Promise<Profile>
  getPublicProfile(slug: string): Promise<PublicProfile>
}
