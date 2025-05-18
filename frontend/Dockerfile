# Этап сборки
FROM node:18-alpine

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./
RUN npm ci

# Копируем .env файл из корневой директории
COPY .env ./

# Копируем исходный код frontend
COPY frontend/ .

# Собираем приложение
RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
