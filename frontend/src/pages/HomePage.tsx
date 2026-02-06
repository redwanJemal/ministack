import { Link } from 'react-router-dom';
import { useTelegram } from '@/lib/telegram';
import { User, Settings, Zap, Star, CheckCircle, Database } from 'lucide-react';

interface Props {
  user: {
    id: string;
    telegram_id: number;
    username: string | null;
    first_name: string;
    last_name: string | null;
    photo_url: string | null;
    is_premium: boolean;
  } | null;
}

export function HomePage({ user }: Props) {
  const { haptic, colorScheme } = useTelegram();

  const handleFeatureClick = () => {
    haptic.impact('medium');
    // Add your feature logic here
  };

  return (
    <div className="container py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold">
            Welcome{user ? `, ${user.first_name}` : ''}! 👋
          </h1>
          <p className="text-tg-hint text-sm mt-1">
            Your Mini App is ready
          </p>
        </div>
        <Link
          to="/profile"
          className="w-10 h-10 rounded-full bg-tg-secondary-bg flex items-center justify-center"
          onClick={() => haptic.selection()}
        >
          {user?.photo_url ? (
            <img
              src={user.photo_url}
              alt={user.first_name}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            <User className="w-5 h-5 text-tg-hint" />
          )}
        </Link>
      </div>

      {/* Premium Badge */}
      {user?.is_premium && (
        <div className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-lg border border-yellow-500/20 mb-6">
          <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
          <span className="text-sm font-medium">Telegram Premium</span>
        </div>
      )}

      {/* Feature Cards */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold mb-3">Features</h2>
        
        <button
          onClick={handleFeatureClick}
          className="w-full p-4 bg-tg-secondary-bg rounded-xl flex items-center gap-4 active:scale-[0.98] transition-transform"
        >
          <div className="w-12 h-12 rounded-xl bg-tg-button/10 flex items-center justify-center">
            <Zap className="w-6 h-6 text-tg-button" />
          </div>
          <div className="flex-1 text-left">
            <h3 className="font-medium">Quick Action</h3>
            <p className="text-sm text-tg-hint">Tap to trigger haptic feedback</p>
          </div>
        </button>

        <button
          onClick={handleFeatureClick}
          className="w-full p-4 bg-tg-secondary-bg rounded-xl flex items-center gap-4 active:scale-[0.98] transition-transform"
        >
          <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center">
            <Settings className="w-6 h-6 text-green-500" />
          </div>
          <div className="flex-1 text-left">
            <h3 className="font-medium">Settings</h3>
            <p className="text-sm text-tg-hint">Configure your preferences</p>
          </div>
        </button>
      </div>

      {/* Info Section */}
      <div className="mt-8 p-4 bg-tg-secondary-bg rounded-xl">
        <h3 className="font-medium mb-2 flex items-center gap-2">
          <Database className="w-4 h-4" />
          Session Info
        </h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between items-center">
            <span className="text-tg-hint">Auth Status</span>
            <span className="flex items-center gap-1 text-green-500">
              <CheckCircle className="w-4 h-4" />
              {user?.id === 'dev-user' ? 'Demo Mode' : 'Authenticated'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-tg-hint">Theme</span>
            <span className="capitalize">{colorScheme}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-tg-hint">Telegram ID</span>
            <span className="font-mono text-xs">{user?.telegram_id || 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-tg-hint">Username</span>
            <span>@{user?.username || 'none'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-tg-hint">Internal ID</span>
            <span className="font-mono text-xs">{user?.id?.slice(0, 8) || 'N/A'}...</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <p className="text-center text-tg-hint text-xs mt-8">
        Built with MiniStack 🚀
      </p>
    </div>
  );
}
