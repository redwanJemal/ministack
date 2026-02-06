/**
 * API Client for backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Token storage
let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
  if (token) {
    localStorage.setItem('access_token', token);
  } else {
    localStorage.removeItem('access_token');
  }
}

export function getAccessToken(): string | null {
  if (!accessToken) {
    accessToken = localStorage.getItem('access_token');
  }
  return accessToken;
}

// API Error class
export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(message: string, status: number, data?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

// Base fetch function
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}/api/v1${endpoint}`;
  const token = getAccessToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { detail: 'An error occurred' };
    }
    throw new ApiError(
      errorData.detail || 'Request failed',
      response.status,
      errorData
    );
  }

  // Handle empty responses
  const text = await response.text();
  if (!text) return {} as T;

  return JSON.parse(text);
}

// API methods
export const api = {
  get: <T>(endpoint: string) => fetchApi<T>(endpoint, { method: 'GET' }),

  post: <T>(endpoint: string, data?: unknown) =>
    fetchApi<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),

  patch: <T>(endpoint: string, data?: unknown) =>
    fetchApi<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    }),

  put: <T>(endpoint: string, data?: unknown) =>
    fetchApi<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    }),

  delete: <T>(endpoint: string) => fetchApi<T>(endpoint, { method: 'DELETE' }),
};

// Auth API
interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface User {
  id: string;
  telegram_id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  photo_url: string | null;
  is_premium: boolean;
  language_code: string | null;
  settings?: Record<string, unknown>;
}

export const authApi = {
  /**
   * Authenticate with Telegram initData
   */
  login: async (initData: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/telegram', {
      init_data: initData,
    });
    setAccessToken(response.access_token);
    return response;
  },

  /**
   * Get current user
   */
  getMe: () => api.get<User>('/users/me'),

  /**
   * Update user settings
   */
  updateSettings: (settings: Record<string, unknown>) =>
    api.patch<User>('/users/me/settings', { settings }),

  /**
   * Logout (clear token)
   */
  logout: () => {
    setAccessToken(null);
  },
};
