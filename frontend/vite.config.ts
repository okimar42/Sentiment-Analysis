import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import type { ServerOptions } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    https: false, // Let nginx handle HTTPS
    proxy: {
      '/api': {
        target: 'http://nginx:80',
        changeOrigin: true,
        secure: false,
      }
    }
  } as ServerOptions,
  preview: {
    host: '0.0.0.0',
    port: 3000,
  }
})
