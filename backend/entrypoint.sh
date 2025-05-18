#!/bin/bash
set -e

echo "=== Запуск инициализации ==="

# Безопасный вывод DATABASE_URL
echo "DATABASE_URL: ${DATABASE_URL//:[^@]*@/:<hidden>@}"

# Проверка обязательных переменных
if [ -z "$DATABASE_URL" ]; then
    echo "❌ Ошибка: DATABASE_URL не установлена!"
    exit 1
fi

# Извлекаем компоненты подключения
DB_HOST=$(echo $DATABASE_URL | awk -F[@] '{print $2}' | awk -F[:/] '{print $1}')
DB_PORT=5432

echo "🔍 Проверка доступности PostgreSQL на $DB_HOST:$DB_PORT..."

# Альтернативный метод проверки (без /dev/tcp)
timeout 120 bash -c "
    while ! (psql -t -c '\q' 2>/dev/null); do 
        echo '⏳ Ожидание PostgreSQL... ($DB_HOST:$DB_PORT)';
        sleep 2; 
    done
" || {
    echo "❌ Не удалось подключиться к PostgreSQL!"
    echo "Возможные причины:"
    echo "1. Сервис PostgreSQL не запущен или не готов"
    echo "2. Неправильные параметры подключения в DATABASE_URL"
    echo "3. Проблемы с сетью между сервисами"
    echo "4. Ограничения firewall в Render"
    
    # Дополнительная диагностика
    echo "=== ДИАГНОСТИКА ==="
    echo "Попытка разрешения DNS:"
    nslookup $DB_HOST || echo "⚠ Не удалось разрешить имя хоста"
    echo "Попытка ping (может не работать в Render):"
    ping -c 2 $DB_HOST || echo "⚠ Ping не доступен"
    
    exit 1
}

echo "✅ PostgreSQL доступен!"

# Основные команды Django
cd src

echo "🔄 Применение миграций..."
python manage.py migrate

echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя (только для разработки)
if [ "$DJANGO_ENV" != "production" ]; then
    echo "👑 Создание суперпользователя..."
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --password "$DJANGO_SUPERUSER_PASSWORD" 2>/dev/null || \
    echo "ℹ Суперпользователь уже существует или ошибка"
fi

echo "🚀 Запуск Gunicorn..."
exec gunicorn medbook.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile -

# #!/bin/bash
# echo 'Waiting for PostgreSQL...'
# while ! python -c 'import socket; import os; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); result = sock.connect_ex(("db", 5432)); sock.close(); exit(result)'; do 
#   sleep 1
# done

# echo 'PostgreSQL is ready!'
# cd src
# python manage.py migrate
# python manage.py collectstatic --noinput
# python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true
# python manage.py runserver 0.0.0.0:8000


# if ! command -v pg_isready &> /dev/null; then
#     apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
# fi

# echo "Ожидание PostgreSQL..."
# until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -t 5; do
#     echo "Попытка подключения к PostgreSQL..."
#     sleep 5
# done

# python manage.py migrate
# python manage.py collectstatic --noinput


# exec gunicorn medbook.wsgi:application --bind 0.0.0.0:$PORT --timeout 120