// Project types

export type ProjectStatus = 'ACTIVE' | 'STAGING' | 'ARCHIVED';
export type ProjectCategory = 'DEMO' | 'INTERNAL' | 'PRODUCTION';
export type ProjectScale = 'SMALL' | 'MEDIUM' | 'LARGE' | 'ENTERPRISE';

export interface Project {
  id: string;
  profileId: string;
  name: string;
  description: string;
  status: ProjectStatus;
  category: ProjectCategory;
  startDate?: string;
  endDate?: string;
  technologies: string[];
  achievements: string[];
  challenges: string[];
  client?: string;
  scale: ProjectScale;
  createdAt: string;
  updatedAt: string;
}

export interface ProjectCreate {
  name: string;
  description: string;
  status?: ProjectStatus;
  category?: ProjectCategory;
  startDate?: string;
  endDate?: string;
  technologies?: string[];
  achievements?: string[];
  challenges?: string[];
  client?: string;
  scale?: ProjectScale;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: ProjectStatus;
  category?: ProjectCategory;
  startDate?: string;
  endDate?: string;
  technologies?: string[];
  achievements?: string[];
  challenges?: string[];
  client?: string;
  scale?: ProjectScale;
}
