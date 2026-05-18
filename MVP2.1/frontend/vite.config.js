import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite配置
export default defineConfig({
  plugins: [vue()],           // 启用Vue插件
  server: {
    port: 5173,               // 开发服务器端口
    open: true,               // 自动打开浏览器
  }
})