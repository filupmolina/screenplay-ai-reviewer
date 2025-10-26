/**
 * Dev Mode Logger
 *
 * Purpose: Eliminate the "what error?" back-and-forth during debugging.
 *
 * In development:
 * - Logs EVERYTHING with full context
 * - Groups related logs for readability
 * - Shows request/response data
 * - Displays stack traces
 *
 * In production:
 * - Silent (or sends to Sentry)
 * - Minimal performance impact
 *
 * Usage:
 *   import { logger } from '@/lib/logger'
 *   logger.error('Task fetch failed', error, { taskId: '123' })
 *   logger.api('GET', '/api/tasks', 200, data)
 *   logger.debug('User clicked button', { userId })
 */

const isDev = import.meta.env.DEV || import.meta.env.MODE === 'development'

// Optional: Allow runtime toggle via localStorage
const isLoggingEnabled = () => {
  if (!isDev) return false
  const devLogs = localStorage.getItem('dev_logs')
  return devLogs === null || devLogs === 'true' // enabled by default
}

export const logger = {
  /**
   * Log errors with full context
   * Shows: error message, stack trace, metadata
   * Always visible in dev, sent to Sentry in production
   */
  error: (context: string, error: any, metadata?: any) => {
    if (!isLoggingEnabled()) return

    console.group(`❌ ERROR: ${context}`)
    console.error('Error:', error)

    if (error?.stack) {
      console.error('Stack:', error.stack)
    }

    if (error?.message) {
      console.error('Message:', error.message)
    }

    if (metadata) {
      console.error('Metadata:', metadata)
    }

    console.groupEnd()

    // TODO: In production, send to Sentry
    // if (import.meta.env.PROD) {
    //   Sentry.captureException(error, { contexts: { metadata } })
    // }
  },

  /**
   * Debug logs - only in dev mode
   * Use for tracking flow, state changes, user actions
   */
  debug: (context: string, data?: any) => {
    if (!isLoggingEnabled()) return

    if (data !== undefined) {
      console.log(`🔍 ${context}:`, data)
    } else {
      console.log(`🔍 ${context}`)
    }
  },

  /**
   * API call logging - request and response
   * Shows: method, URL, status, response data
   * Makes network debugging instant
   */
  api: (method: string, url: string, status: number, data?: any) => {
    if (!isLoggingEnabled()) return

    const statusEmoji = status >= 200 && status < 300 ? '✅' : '❌'

    console.group(`${statusEmoji} API ${method} ${url} (${status})`)
    console.log('Status:', status)

    if (data !== undefined) {
      console.log('Data:', data)
    }

    console.groupEnd()
  },

  /**
   * State change logging
   * Shows: what changed, before/after values
   * Useful for tracking Zustand/Redux updates
   */
  state: (action: string, before?: any, after?: any) => {
    if (!isLoggingEnabled()) return

    console.group(`📊 STATE: ${action}`)

    if (before !== undefined) {
      console.log('Before:', before)
    }

    if (after !== undefined) {
      console.log('After:', after)
    }

    console.groupEnd()
  },

  /**
   * User action logging
   * Track what users do for debugging flows
   */
  action: (action: string, details?: any) => {
    if (!isLoggingEnabled()) return

    if (details !== undefined) {
      console.log(`👆 USER ACTION: ${action}`, details)
    } else {
      console.log(`👆 USER ACTION: ${action}`)
    }
  },

  /**
   * Performance logging
   * Track slow operations
   */
  perf: (label: string, durationMs: number, threshold = 1000) => {
    if (!isLoggingEnabled()) return

    const emoji = durationMs > threshold ? '🐌' : '⚡'
    console.log(`${emoji} PERF: ${label} took ${durationMs}ms`)
  },

  /**
   * Warning logs
   * Non-critical issues that should be investigated
   */
  warn: (context: string, data?: any) => {
    if (!isLoggingEnabled()) return

    console.group(`⚠️ WARNING: ${context}`)
    if (data !== undefined) {
      console.warn('Details:', data)
    }
    console.groupEnd()
  },

  /**
   * Info logs
   * General information, success messages
   */
  info: (message: string, data?: any) => {
    if (!isLoggingEnabled()) return

    if (data !== undefined) {
      console.info(`ℹ️ ${message}`, data)
    } else {
      console.info(`ℹ️ ${message}`)
    }
  }
}

/**
 * Performance timer utility
 * Usage:
 *   const timer = logger.startTimer('API call')
 *   await fetchData()
 *   timer.end()
 */
logger.startTimer = (label: string) => {
  const start = performance.now()

  return {
    end: () => {
      const duration = performance.now() - start
      logger.perf(label, duration)
      return duration
    }
  }
}

/**
 * Helper: Create scoped logger
 * Automatically prefixes all logs with component/module name
 *
 * Usage:
 *   const log = logger.scope('TaskList')
 *   log.debug('Component mounted')
 *   // Output: 🔍 [TaskList] Component mounted
 */
logger.scope = (scopeName: string) => ({
  error: (context: string, error: any, metadata?: any) =>
    logger.error(`[${scopeName}] ${context}`, error, metadata),
  debug: (context: string, data?: any) =>
    logger.debug(`[${scopeName}] ${context}`, data),
  api: (method: string, url: string, status: number, data?: any) =>
    logger.api(method, url, status, data),
  state: (action: string, before?: any, after?: any) =>
    logger.state(`[${scopeName}] ${action}`, before, after),
  action: (action: string, details?: any) =>
    logger.action(`[${scopeName}] ${action}`, details),
  warn: (context: string, data?: any) =>
    logger.warn(`[${scopeName}] ${context}`, data),
  info: (message: string, data?: any) =>
    logger.info(`[${scopeName}] ${message}`, data)
})
