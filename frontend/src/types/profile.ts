// Profile types matching backend schemas (camelCase)

export interface Profile {
  id: string;
  userId: string;
  slug?: string;
  headline?: string;
  summary?: string;
  location?: string;
  visibility: 'PRIVATE' | 'FRIENDS' | 'PUBLIC';
  contact: Record<string, any>;
  profilePhotoUrl?: string;
  completenessScore: number;
  createdAt: string;
  updatedAt?: string;
  draftData?: Record<string, any>;
}

export interface ProfileCreate {
  headline?: string;
  summary?: string;
  location?: string;
  visibility?: 'PRIVATE' | 'FRIENDS' | 'PUBLIC';
  contact?: Record<string, any>;
  profilePhotoUrl?: string;
  slug?: string;
  draftData?: Record<string, any>;
}

export interface ProfileUpdate {
  headline?: string;
  summary?: string;
  location?: string;
  visibility?: 'PRIVATE' | 'FRIENDS' | 'PUBLIC';
  contact?: Record<string, any>;
  profilePhotoUrl?: string;
  draftData?: Record<string, any>;
}

export interface ProfileSummary {
  id: string;
  headline?: string;
  location?: string;
  completenessScore: number;
  visibility: string;
}

export interface ProfilePublic {
  id: string;
  slug?: string;
  headline?: string;
  summary?: string;
  location?: string;
  profilePhotoUrl?: string;
  createdAt: string;
}
