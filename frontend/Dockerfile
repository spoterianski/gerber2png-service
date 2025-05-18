# Этап сборки
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Создаем простой сервер для отдачи статики (временное решение)
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
