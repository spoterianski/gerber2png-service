# Этап сборки и тестирования
FROM python:3.11-slim as builder

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и тесты
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY pyproject.toml printers.json ./

# Добавляем текущую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# Запускаем тесты
RUN pytest tests/ -v --cov=src --cov-report=term-missing

# Финальный этап
FROM python:3.11-slim

WORKDIR /app

# Копируем только необходимые файлы из builder
COPY --from=builder /app/src/ /app/src/
COPY --from=builder /app/pyproject.toml /app/printers.json ./
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]