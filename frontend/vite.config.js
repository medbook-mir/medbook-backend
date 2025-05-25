import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const allowedHost = process.env.VITE_ALLOWED_HOST

export default defineConfig({
  plugins: [react()],
  root: '/app',
  server: {
    port: 3000,
    host: true,
    allowedHosts: allowedHost ? [allowedHost] : []
  },
  esbuild: {
    target: 'esnext'
  }
})
