export interface UploadFile {
  file: File;
  name: string;
  size: number;
  type: string;
}

export interface CVParseResponse {
  success: boolean;
  data: {
    skills: string[];
    experience: string[];
    certifications: string[];
    education: string[];
  };
}

export interface JobMatch {
  job: {
    id: string;
    title: string;
    company: string;
    location: string;
    salary_range: {
      min: number;
      max?: number;
    };
    description: string;
    employment_type: string;
    url?: string;
  };
  score_details: {
    total_score: number;
    category_scores: Record<string, number>;
    matched_keywords: string[];
    cv_relevance: number;
    high_priority: boolean;
  };
  status: string;
  status_history: Array<{
    status: string;
    timestamp: string;
    notes?: string;
  }>;
  timestamp: string;
}

export interface JobMatchResponse {
  success: boolean;
  matches: JobMatch[];
  timestamp: string;
}

export interface UserProfile {
  user_id: string;
  cv_data: {
    skills: string[];
    experience: string[];
    certifications: string[];
    education: string[];
  };
  email?: string;
  preferences?: {
    job_types?: string[];
    min_salary?: number;
    currency?: string;
    notifications?: {
      email?: boolean;
      daily_summary?: boolean;
    };
  };
  last_updated: string;
}

export interface ProfileResponse {
  success: boolean;
  profile: UserProfile;
}

export interface NotificationTestResponse {
  success: boolean;
  results: {
    job_notifications: {
      success: number;
      failed: number;
      total: number;
    };
    pr_notifications: boolean[];
  };
  message: string;
}

export interface SlackConfigResponse {
  success: boolean;
  message: string;
}
