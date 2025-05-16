import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url';
import { configDefaults } from 'vitest/config';
import svgLoader from 'vite-svg-loader';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    svgLoader(),
    mode === 'analyze' && visualizer({ open: true, gzipSize: true })
  ].filter(Boolean),

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@assets': fileURLToPath(new URL('./src/assets', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@composables': fileURLToPath(new URL('./src/composables', import.meta.url)),
      '@stores': fileURLToPath(new URL('./src/stores', import.meta.url)),
      '@utils': fileURLToPath(new URL('./src/utils', import.meta.url)),
      '@views': fileURLToPath(new URL('./src/views', import.meta.url)),
      '@types': fileURLToPath(new URL('./src/types', import.meta.url)),
      '@router': fileURLToPath(new URL('./src/router', import.meta.url)),
      '@layouts': fileURLToPath(new URL('./src/layouts', import.meta.url)),
    },
  },

  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },

  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          vendors: ['axios', 'lodash'],
          charts: ['chart.js', 'vue-chartjs'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @use "@assets/styles/variables.scss" as *;
          @use "@assets/styles/mixins.scss" as *;
        `,
      },
    },
  },

  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      all: true,
      include: ['src/**/*.{ts,vue}'],
      exclude: [
        ...configDefaults.exclude,
        '**/e2e/**',
        '**/*.d.ts',
        '**/main.ts',
        '**/__tests__/**',
        '**/types/**',
        '**/stories/**',
      ],
    },
    exclude: [...configDefaults.exclude, '**/e2e/**'],
  },

  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      '@vueuse/core',
    ],
  },
}));
