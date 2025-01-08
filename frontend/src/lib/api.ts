import {
  type UploadFile,
  type CVParseResponse,
  type JobMatchResponse,
  type ProfileResponse,
  type UserProfile,
  type NotificationTestResponse,
  type SlackConfigResponse,
} from '../types/files';

const API_BASE_URL = '';

/**
 * Parse a CV file and extract structured data
 */
export async function parseCV(file: File): Promise<CVParseResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/parse-cv`, {
    method: 'POST',
    body: formData,
    credentials: 'omit'
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to parse CV');
  }

  return response.json();
}

/**
 * Get job matches for a user
 */
export async function getJobMatches(
  userId: string,
  options: {
    remoteOnly?: boolean;
    minSalary?: number | null;
    employmentTypes?: string[];
  } = {}
): Promise<JobMatchResponse> {
  const params = new URLSearchParams({
    remote_only: String(options.remoteOnly ?? true),
    min_salary: String(options.minSalary ?? 100000),
    ...(options.employmentTypes && {
      employment_types: options.employmentTypes.join(','),
    }),
  });

  const response = await fetch(
    `${API_BASE_URL}/api/jobs/match/${userId}?${params.toString()}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'omit'
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch job matches');
  }

  return response.json();
}

/**
 * Create or update a user profile
 */
export async function updateProfile(profileData: {
  userId: string;
  cvData: UserProfile['cv_data'];
  email?: string;
  preferences?: UserProfile['preferences'];
}): Promise<ProfileResponse> {
  const response = await fetch(`${API_BASE_URL}/api/profiles`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profileData),
    credentials: 'omit',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update profile');
  }

  return response.json();
}

/**
 * Get a user profile by ID
 */
export async function getProfile(
  userId: string
): Promise<ProfileResponse> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${userId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'omit',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch profile');
  }

  return response.json();
}

/**
 * Test Slack notifications (jobs and PRs)
 */
export async function testNotifications(): Promise<NotificationTestResponse> {
  const response = await fetch(`${API_BASE_URL}/api/test/notifications`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'omit',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to test notifications');
  }

  return response.json();
}

/**
 * Configure Slack integration with webhook URL
 */
export async function configureSlack(credentials: {
  client_id: string;
  client_secret: string;
}): Promise<SlackConfigResponse> {
  const response = await fetch(`${API_BASE_URL}/api/config/slack`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
    credentials: 'omit',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to configure Slack');
  }

  return response.json();
}
