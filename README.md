markdown

# Проект: [Название проекта]

## 🚀 Быстрый старт

### Установка зависимостей
```bash
npm install

Запуск разработки
bash

npm run dev

Сборка для production
bash

npm run build

Запуск тестов
bash

npm run test

🏗️ Структура проекта

src/
├── assets/               # Статические ресурсы
│   └── styles/           # Глобальные стили
│       ├── base.css      # Базовые стили
│       ├── utilities.css # Вспомогательные классы
│       └── variables.css # CSS-переменные
│
├── components/           # UI-компоненты
│   ├── icons/            # SVG-иконки
│   └── ui/               # Базовые компоненты (Button, Input и др.)
│
├── composables/          # Composition API хуки
│   └── api/              # API-методы
│
├── features/             # Функциональные компоненты
│   ├── Auth/             # Авторизация
│   ├── Dashboard/        # Дашборд
│   └── Requests/         # Работа с заявками
│
├── stores/               # Хранилища Pinia
├── types/                # Типы TypeScript
└── views/                # Страницы приложения

📝 Правила разработки
1. Работа с компонентами

    UI-компоненты → /components/ui/

    Иконки → /components/icons/

    Бизнес-компоненты → /features/

Пример:
javascript

// Правильно
import AppButton from '@/components/ui/AppButton.vue'
import { useAuth } from '@/features/Auth/composables/useAuth'

2. Работа с API

    Каждая сущность имеет свой файл в composables/api/

    Используйте готовый хук useFetch

Пример:
typescript

// composables/api/posts.api.ts
export const usePostsApi = () => {
  const fetchPosts = () => useFetch('/api/posts')
  return { fetchPosts }
}

3. Стилизация

    Глобальные переменные → variables.css

    Утилитарные классы → utilities.css

    Компонентные стили → <style scoped> в компоненте

🔧 Code Quality
Линтинг
bash

npm run lint

Форматирование
bash

npm run format

Pre-commit хуки

    Автоматически запускают линтинг

    Проверяют соответствие структуре проекта

🛠 Технологический стек

    Vue 3 + TypeScript

    Pinia (стейт-менеджмент)

    Vite (сборка)

    Vitest (тестирование)

    ESLint + Prettier (линтеры)

🤝 Участие в разработке

    Создайте ветку от main

    Следуйте соглашениям о структуре

    Откройте Pull Request с описанием изменений

📜 Лицензия

MIT