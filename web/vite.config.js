import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'configure-server',
      configureServer(server) {
        // Serve episode files from parent directory
        server.middlewares.use((req, res, next) => {
          if (req.url.startsWith('/episodes/')) {
            const episodePath = req.url.replace('/episodes/', '')
            req.url = '/@fs/' + path.resolve(__dirname, '..', episodePath)
          }
          next()
        })
      }
    }
  ],
  server: {
    fs: {
      // Allow serving files from parent directory (episode folders)
      allow: ['..']
    }
  },
  publicDir: 'public',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@episodes': path.resolve(__dirname, '..')
    }
  }
})
