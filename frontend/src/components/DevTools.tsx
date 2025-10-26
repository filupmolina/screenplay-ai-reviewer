/**
 * Dev Tools Component
 *
 * Provides runtime controls for development features:
 * - Toggle verbose logging on/off
 * - Only visible in development mode
 * - Settings persist in localStorage
 *
 * Usage:
 *   // Add to your app root (after ThemeProvider)
 *   <DevTools />
 *
 * This will show a small floating button in bottom-right corner.
 */

import { useState } from 'react'

export function DevTools() {
  const [logsEnabled, setLogsEnabled] = useState(() => {
    const stored = localStorage.getItem('dev_logs')
    return stored === null || stored === 'true' // enabled by default
  })

  const [isOpen, setIsOpen] = useState(false)

  // Only show in development
  if (import.meta.env.PROD || import.meta.env.MODE === 'production') {
    return null
  }

  const toggleLogs = () => {
    const newValue = !logsEnabled
    localStorage.setItem('dev_logs', String(newValue))
    setLogsEnabled(newValue)
    // Reload to apply logging changes
    window.location.reload()
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {isOpen ? (
        <div className="bg-gray-900 text-white rounded-lg shadow-xl p-4 min-w-[200px]">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-sm">Dev Tools</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          <div className="space-y-2">
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-sm">Verbose Logs</span>
              <input
                type="checkbox"
                checked={logsEnabled}
                onChange={toggleLogs}
                className="ml-3"
              />
            </label>

            <div className="text-xs text-gray-400 mt-2 pt-2 border-t border-gray-700">
              Changes require reload
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gray-900 text-white px-3 py-2 rounded-lg shadow-lg text-xs font-mono hover:bg-gray-800 transition-colors"
          title="Dev Tools"
        >
          🔧 DEV
        </button>
      )}
    </div>
  )
}
