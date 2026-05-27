FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=museum_project.settings

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Копирование проекта
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

# Сбор статики (будет выполнена при запуске)
RUN python manage.py collectstatic --noinput || true

# Создание непривилегированного пользователя
RUN adduser --disabled-password --no-create-home django-user
RUN chown -R django-user:django-user /app
USER django-user

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "museum_project.wsgi:application"]