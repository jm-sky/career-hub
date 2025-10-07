// Authentication API functions using axios client

import apiClient from './api-client';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  TokenResponse,
  User,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  MessageResponse,
} from '@/types/auth';

export const authAPI = {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const { data } = await apiClient.post<LoginResponse>('/auth/login', credentials);
    return data;
  },

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<LoginResponse> {
    const { data } = await apiClient.post<LoginResponse>('/auth/register', userData);
    return data;
  },

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const { data} = await apiClient.post<TokenResponse>('/auth/refresh', {
      refreshToken,
    });
    return data;
  },

  /**
   * Get current user information
   */
  async getCurrentUser(): Promise<User> {
    const { data } = await apiClient.get<User>('/auth/me');
    return data;
  },

  /**
   * Logout user (server-side logout)
   */
  async logout(): Promise<void> {
    await apiClient.post('/auth/logout');
  },

  /**
   * Request password reset
   */
  async forgotPassword(request: ForgotPasswordRequest): Promise<MessageResponse> {
    const { data } = await apiClient.post<MessageResponse>('/auth/forgot-password', request);
    return data;
  },

  /**
   * Reset password with token
   */
  async resetPassword(request: ResetPasswordRequest): Promise<MessageResponse> {
    const { data } = await apiClient.post<MessageResponse>('/auth/reset-password', request);
    return data;
  },

  /**
   * Change password (authenticated)
   */
  async changePassword(request: ChangePasswordRequest): Promise<MessageResponse> {
    const { data } = await apiClient.post<MessageResponse>('/auth/change-password', request);
    return data;
  },
};
