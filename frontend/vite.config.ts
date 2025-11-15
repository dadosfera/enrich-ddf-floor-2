import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Get API URL from environment variable or use default
const API_URL = process.env.VITE_API_URL || 'http://127.0.0.1:8247'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: API_URL,
        changeOrigin: true,
        secure: false,
      },
      '/health': {
        target: API_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
