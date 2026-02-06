/**
 * Full-screen loading indicator
 */
export default function LoadingScreen() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-tg-bg">
      <p className="text-5xl mb-4">🛒</p>
      <h1 className="text-2xl font-bold text-tg-text">ገበያ</h1>
      <p className="text-sm text-tg-hint mt-1">Ethiopian Marketplace</p>
      <div className="w-8 h-8 border-3 border-tg-button border-t-transparent rounded-full animate-spin mt-6" />
    </div>
  );
}
