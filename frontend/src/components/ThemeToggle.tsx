/**
 * Theme Toggle Component
 *
 * Simple button to toggle between light and dark mode.
 * Place in header, navbar, or as floating button.
 *
 * Usage:
 *   import { ThemeToggle } from '@/components/ThemeToggle'
 *
 *   <header>
 *     <h1>My App</h1>
 *     <ThemeToggle />
 *   </header>
 *
 * Note: Requires lucide-react for icons
 *   npm install lucide-react
 */

import { Moon, Sun } from 'lucide-react'
import { useTheme } from '@/providers/ThemeProvider'

export function ThemeToggle() {
  const { actualTheme, setTheme } = useTheme()

  const toggleTheme = () => {
    // Toggle between light and dark (ignoring 'system' for simplicity)
    setTheme(actualTheme === 'dark' ? 'light' : 'dark')
  }

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg hover:bg-muted transition-colors"
      title={`Switch to ${actualTheme === 'dark' ? 'light' : 'dark'} mode`}
      aria-label={`Switch to ${actualTheme === 'dark' ? 'light' : 'dark'} mode`}
    >
      {actualTheme === 'dark' ? (
        <Sun className="h-5 w-5" />
      ) : (
        <Moon className="h-5 w-5" />
      )}
    </button>
  )
}

/**
 * Alternative: Dropdown with system option
 *
 * If you want users to choose between light/dark/system:
 */
export function ThemeToggleDropdown() {
  const { theme, setTheme } = useTheme()

  return (
    <select
      value={theme}
      onChange={(e) => setTheme(e.target.value as 'light' | 'dark' | 'system')}
      className="px-3 py-2 rounded-lg bg-background border border-border"
    >
      <option value="light">Light</option>
      <option value="dark">Dark</option>
      <option value="system">System</option>
    </select>
  )
}
