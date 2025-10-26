/**
 * VersionDisplay Component
 *
 * Shows app version in bottom-left corner for debugging and cache verification.
 *
 * Features:
 * - Displays version from package.json
 * - Shows (dev) indicator in development
 * - Very subtle styling (doesn't interfere with UI)
 * - Always visible for quick reference
 *
 * Usage:
 * ```tsx
 * import { VersionDisplay } from '@/components/VersionDisplay'
 *
 * function App() {
 *   return (
 *     <>
 *       <VersionDisplay />
 *       {/* rest of app *\/}
 *     </>
 *   )
 * }
 * ```
 */

export function VersionDisplay() {
  const version = import.meta.env.VITE_APP_VERSION || '0.0.0'
  const buildTime = import.meta.env.VITE_BUILD_TIME || 'unknown'
  const isDev = import.meta.env.DEV

  // Format: "12:34:56" from ISO timestamp
  const timeOnly = buildTime !== 'unknown' ? new Date(buildTime).toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }) : 'unknown'

  return (
    <div
      className="fixed bottom-2 left-2 text-xs text-muted-foreground/50 font-mono select-none z-50"
      title={`Version ${version} | Build: ${buildTime}${isDev ? ' (dev mode)' : ''}`}
    >
      v{version} • {timeOnly} {isDev && '(dev)'}
    </div>
  )
}
