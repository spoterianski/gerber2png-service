# Этап сборки
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

# Копируем .env файл
COPY .env ./

# Копируем исходный код
COPY . .

# Собираем приложение (переменные окружения будут доступны при сборке)
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
