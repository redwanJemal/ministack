/**
 * Full-screen loading indicator
 */
export function LoadingScreen() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-tg-bg">
      <div className="w-12 h-12 border-4 border-tg-button border-t-transparent rounded-full animate-spin" />
      <p className="mt-4 text-tg-hint text-sm">Loading...</p>
    </div>
  );
}
