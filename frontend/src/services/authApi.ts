import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export interface LoginCredentials {
  email: string;
  password: string;
  remember?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  national_id: string;
  // השדות הבאים יתווספו בטופס הפרופיל האישי מאוחר יותר
  // city?: string;
  // street?: string;
  // building?: string;
  // entrance?: string;
  // postal_code?: string;
  // date_of_birth?: Date;
  // phone_number?: string;
}

export interface ResetPasswordRequest {
  email: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
  }
}

const authApi = {
  login: async (credentials: LoginCredentials) => {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/api/auth/login`, 
      credentials
    );
    
    // Store token if remember me is checked
    if (credentials.remember) {
      localStorage.setItem('token', response.data.access_token);
    } else {
      sessionStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },
  
  register: async (userData: RegisterData) => {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/api/auth/register`, 
      userData
    );
    return response.data;
  },
  
  forgotPassword: async (request: ResetPasswordRequest) => {
    const response = await axios.post(
      `${API_URL}/api/auth/password-reset-request`, 
      request
    );
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
  },
  
  getToken: (): string | null => {
    return localStorage.getItem('token') || sessionStorage.getItem('token');
  },
  
  isAuthenticated: (): boolean => {
    return !!authApi.getToken();
  }
};

export default authApi; 