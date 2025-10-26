import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  define: {
    // App version from package.json (for releases)
    'import.meta.env.VITE_APP_VERSION': JSON.stringify(process.env.npm_package_version),
    // Build timestamp - changes every time dev server restarts (for cache verification)
    'import.meta.env.VITE_BUILD_TIME': JSON.stringify(new Date().toISOString()),
  },
})
