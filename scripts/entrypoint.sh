#!/bin/sh
set -e

# Компиляция статических файлов
echo "Collecting static files..." # нету статических файлов
python manage.py collectstatic --noinput


# Применение миграций базы данных
echo "Applying database migrations..."
python manage.py makemigrations --noinput  # Применение миграций
python manage.py migrate --noinput  # Применение миграций

# Запуск uwsgi-сервера
#echo "Starting uwsgi server..."
#uwsgi --socket :8000 --master --enable-threads --module core.wsgi


# Получаем значение порта из переменной окружения
echo "Starting Django development server on port ${DRF_HOST}:${DRF_PORT}..."
python manage.py runserver ${DRF_HOST}:${DRF_PORT}
