import { useNavigate } from 'react-router-dom';
import { useTelegram, useBackButton } from '@/lib/telegram';
import { User, Star, Globe, LogOut } from 'lucide-react';
import { authApi } from '@/lib/api';
import { toast } from 'sonner';

interface Props {
  user: {
    id: string;
    telegram_id: number;
    username: string | null;
    first_name: string;
    last_name: string | null;
    photo_url: string | null;
    is_premium: boolean;
    language_code?: string | null;
  } | null;
}

export function ProfilePage({ user }: Props) {
  const navigate = useNavigate();
  const { haptic, showConfirm } = useTelegram();

  // Setup back button
  useBackButton(() => {
    haptic.selection();
    navigate(-1);
  });

  const handleLogout = async () => {
    haptic.impact('medium');
    const confirmed = await showConfirm('Are you sure you want to logout?');
    if (confirmed) {
      authApi.logout();
      toast.success('Logged out successfully');
      window.location.reload();
    }
  };

  if (!user) {
    return (
      <div className="container py-6">
        <p className="text-center text-tg-hint">Not logged in</p>
      </div>
    );
  }

  return (
    <div className="container py-6">
      {/* Profile Header */}
      <div className="flex flex-col items-center mb-8">
        <div className="w-24 h-24 rounded-full bg-tg-secondary-bg flex items-center justify-center mb-4 overflow-hidden">
          {user.photo_url ? (
            <img
              src={user.photo_url}
              alt={user.first_name}
              className="w-full h-full object-cover"
            />
          ) : (
            <User className="w-12 h-12 text-tg-hint" />
          )}
        </div>
        <h1 className="text-xl font-bold">
          {user.first_name} {user.last_name}
        </h1>
        {user.username && (
          <p className="text-tg-hint">@{user.username}</p>
        )}
        {user.is_premium && (
          <div className="flex items-center gap-1 mt-2 px-3 py-1 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 rounded-full">
            <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
            <span className="text-sm font-medium text-yellow-600">Premium</span>
          </div>
        )}
      </div>

      {/* Profile Info */}
      <div className="bg-tg-secondary-bg rounded-xl overflow-hidden mb-6">
        <div className="p-4 border-b border-tg-bg/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-tg-button/10 flex items-center justify-center">
              <User className="w-5 h-5 text-tg-button" />
            </div>
            <div className="flex-1">
              <p className="text-sm text-tg-hint">Telegram ID</p>
              <p className="font-mono">{user.telegram_id}</p>
            </div>
          </div>
        </div>
        
        {user.language_code && (
          <div className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-500/10 flex items-center justify-center">
                <Globe className="w-5 h-5 text-green-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-tg-hint">Language</p>
                <p className="uppercase">{user.language_code}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="space-y-3">
        <button
          onClick={handleLogout}
          className="w-full p-4 bg-tg-destructive/10 text-tg-destructive rounded-xl flex items-center justify-center gap-2 active:scale-[0.98] transition-transform"
        >
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Logout</span>
        </button>
      </div>

      {/* App Version */}
      <p className="text-center text-tg-hint text-xs mt-8">
        MiniStack v1.0.0
      </p>
    </div>
  );
}
