import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    // This is required to make the server accessible from outside the container
    host: '0.0.0.0',
    // This is required for HMR to work in a Docker container
    hmr: {
      clientPort: 5173,
    },
    // This is required for file changes to be detected in a Docker container
    watch: {
      usePolling: true,
    },
  },
})
