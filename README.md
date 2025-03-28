# DOWNLOADER-AUDIO-API


REST API для загрузки и конвертации аудио из различных источников, построенный с использованием FastAPI.

## Возможности

- Загрузка аудио на сервер
- Поиск аудио по ID
- Получение метаданных аудио
- Аутентификация пользователей через яндекс

## Технологии

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Python
- Docker
- Docker Compose


## Структура проекта

```
src/
├── core/           # Основные настройки и конфигурации
├── crud/           # CRUD операции для работы с базой данных
├── models/         # SQLAlchemy модели
├── routers/        # API эндпоинты
├── schemas/        # Pydantic модели
├── service/        # Бизнес-логика
├── settings.py     # Настройки приложения
└── _create_db.py   # Скрипт для создания базы данных
```

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/mister_goyda/downloader-audio-api.git
cd downloader-audio-api
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
```

5. Создайте базу данных:
```bash
python src/_create_db.py
```

6. Запустите приложение:
```bash
uvicorn src.main:app --reload
```

### Запуск через Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose

2. Клонируйте репозиторий:
```bash
git clone https://github.com/mister_goyda/downloader-audio-api.git
cd downloader-audio-api
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up -d
```

После запуска будут доступны следующие сервисы:
- API приложение: `http://localhost:8000`
- Swagger документация: `http://localhost:8000/docs`
- Adminer (управление базой данных): `http://localhost:8080`
  - Система: PostgreSQL
  - Сервер: db
  - Пользователь: postgres
  - Пароль: postgres
  - База данных: audio_downloader

Для остановки приложения:
```bash
docker-compose down
```

## Авторы

- SmellsBa11s - [GitHub](https://github.com/SmellsBa11s)

