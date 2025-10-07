// Experience types matching backend schemas (camelCase)

export interface Experience {
  id: string;
  profileId: string;
  companyName: string;
  companyWebsite?: string;
  companySize?: string;
  industry?: string;
  companyLocation?: string;
  position: string;
  employmentType?: string;
  startDate: string; // ISO date string
  endDate?: string; // ISO date string
  isCurrent: boolean;
  description?: string;
  responsibilities: string[];
  technologies: string[];
  displayOrder: number;
  durationMonths?: number;
  durationText: string;
  createdAt: string;
  updatedAt?: string;
}

export interface ExperienceCreate {
  companyName: string;
  companyWebsite?: string;
  companySize?: string;
  industry?: string;
  companyLocation?: string;
  position: string;
  employmentType?: string;
  startDate: string; // ISO date string
  endDate?: string; // ISO date string
  isCurrent?: boolean;
  description?: string;
  responsibilities?: string[];
  technologies?: string[];
  displayOrder?: number;
}

export interface ExperienceUpdate {
  companyName?: string;
  companyWebsite?: string;
  companySize?: string;
  industry?: string;
  companyLocation?: string;
  position?: string;
  employmentType?: string;
  startDate?: string; // ISO date string
  endDate?: string; // ISO date string
  isCurrent?: boolean;
  description?: string;
  responsibilities?: string[];
  technologies?: string[];
  displayOrder?: number;
}

export interface ExperienceSummary {
  id: string;
  companyName: string;
  position: string;
  startDate: string; // ISO date string
  endDate?: string; // ISO date string
  isCurrent: boolean;
  durationText: string;
  technologies: string[];
}

// Form data types for React Hook Form
export interface ExperienceFormData {
  companyName: string;
  companyWebsite?: string;
  companySize?: string;
  industry?: string;
  companyLocation?: string;
  position: string;
  employmentType?: string;
  startDate: string;
  endDate?: string;
  isCurrent: boolean;
  description?: string;
  responsibilities: string[];
  technologies: string[];
}
