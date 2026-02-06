import { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { useTelegram } from './lib/telegram';
import { authApi, getAccessToken } from './lib/api';
import { HomePage } from './pages/HomePage';
import { ProfilePage } from './pages/ProfilePage';
import { LoadingScreen } from './components/LoadingScreen';

interface User {
  id: string;
  telegram_id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  photo_url: string | null;
  is_premium: boolean;
}

export default function App() {
  const { isReady, initData, isInTelegram } = useTelegram();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function authenticate() {
      if (!isReady) return;

      try {
        // Check for existing token
        const existingToken = getAccessToken();
        if (existingToken) {
          try {
            const userData = await authApi.getMe();
            setUser(userData);
            setIsLoading(false);
            return;
          } catch {
            // Token invalid, continue to login
          }
        }

        // Login with Telegram initData
        if (initData) {
          const response = await authApi.login(initData);
          setUser(response.user);
        } else if (!isInTelegram) {
          // Development mode without Telegram
          console.log('Running outside Telegram - using mock user');
          setUser({
            id: 'dev-user',
            telegram_id: 123456789,
            username: 'dev_user',
            first_name: 'Developer',
            last_name: null,
            photo_url: null,
            is_premium: false,
          });
        } else {
          setError('Unable to authenticate with Telegram');
        }
      } catch (err) {
        console.error('Auth error:', err);
        setError('Authentication failed. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }

    authenticate();
  }, [isReady, initData, isInTelegram]);

  if (isLoading || !isReady) {
    return <LoadingScreen />;
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center">
        <div className="text-4xl mb-4">😕</div>
        <h1 className="text-xl font-bold mb-2">Oops!</h1>
        <p className="text-tg-hint mb-4">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-tg-button text-tg-button-text rounded-lg"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-tg-bg text-tg-text safe-area-top safe-area-bottom">
      <Routes>
        <Route path="/" element={<HomePage user={user} />} />
        <Route path="/profile" element={<ProfilePage user={user} />} />
      </Routes>
    </div>
  );
}
