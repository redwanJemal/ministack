/**
 * Authentication hook for Gebeya
 */

import { useEffect, useState } from 'react';
import { useTelegram } from '@/lib/telegram';
import { authApi, usersApi, setAccessToken, getAccessToken, type User } from '@/lib/api';

export function useAuth() {
  const { initData, isReady, isInTelegram } = useTelegram();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isReady) return;

    const init = async () => {
      setIsLoading(true);
      setError(null);

      try {
        // Check if we have a token
        const existingToken = getAccessToken();
        
        if (existingToken) {
          // Try to get user with existing token
          try {
            const userData = await usersApi.me();
            setUser(userData);
            setIsLoading(false);
            return;
          } catch (e) {
            // Token invalid, clear it
            setAccessToken(null);
          }
        }

        // If in Telegram, login with initData
        if (initData && isInTelegram) {
          const result = await authApi.telegram(initData);
          setAccessToken(result.access_token);
          setUser(result.user);
        } else if (!isInTelegram) {
          // Dev mode - create mock admin user
          console.log('Dev mode: Creating mock user');
          setUser({
            id: 'dev-user',
            telegram_id: 123456789,
            username: 'dev_user',
            first_name: 'Dev',
            last_name: 'User',
            photo_url: null,
            is_premium: false,
            language_code: 'en',
            phone: null,
            is_phone_verified: false,
            city: 'Addis Ababa',
            area: null,
            rating: 0,
            total_sales: 0,
            total_listings: 0,
            is_verified_seller: false,
            is_admin: true,  // Dev is admin
            settings: {},
          });
        }
      } catch (e) {
        console.error('Auth error:', e);
        setError(e instanceof Error ? e.message : 'Authentication failed');
      } finally {
        setIsLoading(false);
      }
    };

    init();
  }, [isReady, initData, isInTelegram]);

  const refreshUser = async () => {
    try {
      const userData = await usersApi.me();
      setUser(userData);
    } catch (e) {
      console.error('Failed to refresh user:', e);
    }
  };

  const logout = () => {
    setAccessToken(null);
    setUser(null);
  };

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    error,
    refreshUser,
    logout,
  };
}
