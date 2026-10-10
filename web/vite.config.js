import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 前端作为独立工程运行，通过 Vite 开发代理把 /api 同源转发到后端 8000 端口。
// 这样浏览器不会触发跨域（后端未开启 CORS），且完全不需要改动任何后端代码。
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Cache-Control', 'no-cache')
            proxyReq.setHeader('Connection', 'keep-alive')
          })
        },
      },
    },
  },
})
