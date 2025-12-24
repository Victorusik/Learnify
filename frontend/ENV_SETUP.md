# Настройка переменных окружения

Для работы с API необходимо создать файлы с переменными окружения.

## Создание файлов

### 1. `.env.development` (для разработки)

Создайте файл `frontend/.env.development` со следующим содержимым:

```
VITE_API_URL=http://localhost:3001/api
```

### 2. `.env.production` (для production/Docker)

Создайте файл `frontend/.env.production` со следующим содержимым:

```
VITE_API_URL=http://backend:3000/api
```

## Примечания

- Vite автоматически загружает переменные окружения с префиксом `VITE_`
- В режиме разработки используется `.env.development`
- При сборке используется `.env.production`
- Эти файлы должны быть добавлены в `.gitignore` (обычно уже там)

## Проверка

После создания файлов перезапустите dev сервер:

```bash
npm run dev
```

Переменная `VITE_API_URL` будет доступна через `import.meta.env.VITE_API_URL`

