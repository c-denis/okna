import js from '@eslint/js';
import globals from 'globals';
import tsParser from '@typescript-eslint/parser';
import vueParser from 'vue-eslint-parser';
import vuePlugin from 'eslint-plugin-vue';
import path from 'path';
import { fileURLToPath } from 'node:url';

// Получаем текущую директорию (аналог __dirname для ES модулей)
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default [
  js.configs.recommended,
  ...vuePlugin.configs['flat/vue3-recommended'],
  {
    files: ['**/*.ts', '**/*.vue'],
    ignores: ['**/node_modules/**', '**/dist/**', '**/*.spec.ts'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        // Глобальные переменные
        test: 'readonly',
        expect: 'readonly',
        describe: 'readonly',
        it: 'readonly',
        ref: 'readonly',
        Ref: 'readonly',
        // Переменные среды Vite
        __dirname: 'readonly',
        __filename: 'readonly',
        import: 'readonly',
        require: 'readonly',
        process: 'readonly',
        import.meta: 'readonly'
      },
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: 'latest',
        sourceType: 'module',
        project: './tsconfig.json',
        tsconfigRootDir: __dirname,
        extraFileExtensions: ['.vue']
      }
    },
    settings: {
      'import/resolver': {
        alias: {
          map: [
            ['@', path.join(__dirname, 'src')],
            ['@components', path.join(__dirname, 'src/components')],
            ['@utils', path.join(__dirname, 'src/utils')]
          ],
          extensions: ['.js', '.ts', '.vue']
        }
      }
    },
    rules: {
      'vue/multi-word-component-names': 'off',
      '@typescript-eslint/no-unused-vars': ['warn', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_',
        destructuredArrayIgnorePattern: '^_'
      }],
      'no-unused-vars': 'off',
      'vue/component-tags-order': ['error', {
        order: ['script', 'template', 'style']
      }],
      'vue/attribute-hyphenation': ['error', 'always']
    }
  },
  {
    files: ['**/*.spec.ts'],
    languageOptions: {
      globals: {
        ...globals.jest, // Если используете Jest-like окружение
        test: 'readonly',
        expect: 'readonly',
        describe: 'readonly',
        it: 'readonly',
        vi: 'readonly' // Для Vitest
      }
    },
    rules: {
      'no-console': 'off',
      '@typescript-eslint/no-explicit-any': 'off'
    }
  }
];