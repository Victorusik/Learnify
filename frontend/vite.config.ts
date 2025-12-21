import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: (content, loaderContext) => {
          // Исключаем сам файл _variables.scss из импорта, чтобы избежать циклического импорта
          if (loaderContext?.resourcePath) {
            const resourcePath = loaderContext.resourcePath.replace(/\\/g, '/')
            // Проверяем, является ли это файлом _variables.scss
            if (resourcePath.includes('_variables.scss') || resourcePath.includes('variables.scss')) {
              return content
            }
          }
          return `@use "@/styles/variables" as *;\n${content}`
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000
  }
})