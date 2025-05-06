# Gerber to PNG Converter

Веб-приложение для конвертации Gerber файлов в PNG формат.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd gerber2png-online
```

2. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up --build
```

3. Откройте браузер и перейдите по адресу:
```
http://localhost:3000
```

## Использование

1. Загрузите Gerber файл (.gbr)
2. Загрузите Drill файл (.drl)
3. Выберите принтер из списка
4. Нажмите кнопку "Конвертировать"
5. Скачайте полученный PNG файл

## Структура проекта

- `backend/` - Python FastAPI бэкенд
- `frontend/` - React TypeScript фронтенд
- `docker-compose.yml` - конфигурация Docker Compose 