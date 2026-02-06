/**
 * Authentication hook using React Query
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authApi, getAccessToken } from '@/lib/api';
import { useTelegram } from '@/lib/telegram';
import { useEffect } from 'react';

interface User {
  id: string;
  telegram_id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  photo_url: string | null;
  is_premium: boolean;
  language_code: string | null;
  settings: Record<string, unknown>;
}

export function useAuth() {
  const queryClient = useQueryClient();
  const { initData, isReady, isInTelegram } = useTelegram();

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: (initData: string) => authApi.login(initData),
    onSuccess: (data) => {
      queryClient.setQueryData(['user'], data.user);
    },
  });

  // Get current user
  const userQuery = useQuery({
    queryKey: ['user'],
    queryFn: authApi.getMe,
    enabled: !!getAccessToken(),
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: false,
  });

  // Auto-login with Telegram initData
  useEffect(() => {
    if (!isReady) return;
    if (userQuery.data) return; // Already logged in
    if (!initData && !isInTelegram) return; // Not in Telegram

    if (initData && !getAccessToken()) {
      loginMutation.mutate(initData);
    }
  }, [isReady, initData, isInTelegram, userQuery.data]);

  // Logout function
  const logout = () => {
    authApi.logout();
    queryClient.clear();
    window.location.reload();
  };

  return {
    user: userQuery.data as User | undefined,
    isLoading: loginMutation.isPending || userQuery.isLoading,
    isAuthenticated: !!userQuery.data,
    error: loginMutation.error || userQuery.error,
    logout,
    refetch: userQuery.refetch,
  };
}
