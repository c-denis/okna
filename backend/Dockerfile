# Базовый образ
FROM python:3.11-slim

# Установка зависимостей (все команды в одном RUN)
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Создаем пользователя и рабочую директорию
RUN useradd -m appuser && \
    mkdir /app && \
    chown appuser:appuser /app

WORKDIR /app
USER appuser

# Копирование и установка зависимостей
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY --chown=appuser:appuser . .

# Команда запуска
CMD ["sh", "-c", "python -m gunicorn --bind 0.0.0.0:8000 crm_core.wsgi:application"]