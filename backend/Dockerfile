# ==============================================
# Базовый образ для сборки зависимостей
# ==============================================
FROM python:3.11-slim as builder

# Установка временных утилит и очистка кеша
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Проверка доступности PyPI с автоматическим переходом на зеркало
RUN for i in 1 2 3; do \
      if curl -s -o /dev/null -w '%{http_code}' https://pypi.org/simple/ | grep -q '200'; then \
        echo "Using official PyPI"; \
        break; \
      elif curl -s -o /dev/null -w '%{http_code}' https://pypi.tuna.tsinghua.edu.cn/simple/ | grep -q '200'; then \
        echo "Using Tsinghua mirror"; \
        echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > /etc/pip.conf; \
        break; \
      fi; \
      if [ $i -eq 3 ]; then exit 1; fi; \
      sleep 5; \
    done

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настройка переменных окружения
ENV PYTHONPATH=/app:/app/apps \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/root/.local/bin:${PATH}"

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --user --no-cache-dir --default-timeout=100 -r requirements.txt

# ==============================================
# Финальный образ
# ==============================================
FROM python:3.11-slim

# Копируем установленные зависимости
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/

# Настройка окружения
ENV PATH="/root/.local/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app:/app/apps \
    DJANGO_SETTINGS_MODULE=config.settings

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app appuser && \
    mkdir -p /app/{static,media} && \
    chown -R appuser:appuser /app

WORKDIR /app

# Копируем код приложения
COPY --chown=appuser:appuser . .

# Проверка зависимостей и путей
RUN python -c "import sys; print('\nPython paths:', sys.path)" && \
    python -c "import django; print('\nDjango version:', django.__version__)" && \
    python -c "from django.conf import settings; print('\nBASE_DIR:', settings.BASE_DIR)" && \
    python -c "from django.conf import settings; print('\nINSTALLED_APPS:', settings.INSTALLED_APPS)" && \
    python -c "import os; print('\nCurrent directory:', os.getcwd())" && \
    python -c "import os; print('\nFiles in /app:', os.listdir('/app'))"

# Порт приложения
EXPOSE 8000

# Команда запуска
USER appuser
CMD ["gunicorn", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "4", \
    "--worker-class", "gevent", \
    "--timeout", "120", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--preload", \
    "config.wsgi:application"]