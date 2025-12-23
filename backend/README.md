# Learnify Backend

Backend API для образовательного приложения Learnify на FastAPI.

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - реляционная база данных
- **Alembic** - миграции базы данных
- **Docker** - контейнеризация

## Структура проекта

```
backend/
├── app/
│   ├── main.py              # FastAPI приложение
│   ├── config.py            # Конфигурация
│   ├── database.py          # Подключение к БД
│   ├── models/              # SQLAlchemy модели
│   ├── schemas/             # Pydantic схемы
│   ├── api/                 # API роутеры
│   ├── services/            # Бизнес-логика
│   ├── utils/               # Утилиты
│   └── seed_data.py         # Скрипт загрузки данных
├── migrations/              # Alembic миграции
├── requirements.txt         # Зависимости
└── Dockerfile               # Docker образ
```

## API Endpoints

### Категории
- `GET /api/categories` - список всех категорий

### Курсы
- `GET /api/courses` - список курсов (опционально: ?category_id=)
- `GET /api/courses/{course_id}` - детали курса
- `POST /api/courses/{course_id}/enroll` - записаться на курс
- `GET /api/courses/{course_id}/lessons` - уроки курса

### Уроки
- `GET /api/lessons/{lesson_id}` - детали урока с блоками

### Пользователь
- `GET /api/user` - данные текущего пользователя
- `PUT /api/user` - обновление данных пользователя
- `GET /api/user/statistics` - статистика пользователя

### Прогресс
- `GET /api/progress` - прогресс пользователя
- `POST /api/progress/block` - отметка блока как выполненного
- `POST /api/progress/lesson` - отметка урока как завершенного

### Тренировка
- `GET /api/training/cards` - карточки для тренировки (spaced repetition)
- `POST /api/training/submit` - отправка ответа на карточку

### Достижения
- `GET /api/achievements` - список всех достижений
- `POST /api/achievements/{achievement_id}/unlock` - разблокировка достижения

## Запуск через Docker

Backend запускается автоматически через `docker-compose up` из корня проекта.

## Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения (создайте `.env`):
```
DATABASE_URL=postgresql://learnify:learnify@localhost:5432/learnify
```

3. Запустите миграции:
```bash
alembic upgrade head
```

4. Загрузите начальные данные:
```bash
python -m app.seed_data
```

5. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу `http://localhost:3001`

## Миграции

Создание новой миграции:
```bash
alembic revision --autogenerate -m "описание изменений"
```

Применение миграций:
```bash
alembic upgrade head
```

Откат миграции:
```bash
alembic downgrade -1
```
