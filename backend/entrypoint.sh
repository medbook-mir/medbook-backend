#!/bin/bash
set -e  

# Безопасный вывод DATABASE_URL (скрываем пароль)
echo "DATABASE_URL: ${DATABASE_URL//:[^@]*@/:<hidden>@}"

# Проверяем, установлена ли переменная DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "Ошибка: DATABASE_URL не установлена!"
    exit 1
fi

# Извлекаем хост и порт из DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | awk -F[@] '{print $2}' | awk -F[:/] '{print $1}')
DB_PORT=5432  # Стандартный порт PostgreSQL

echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT)..."

# Альтернативная проверка доступности порта без nc
timeout 120 bash -c "
    while ! (echo > /dev/tcp/$DB_HOST/$DB_PORT) >/dev/null 2>&1; do 
        echo 'Попытка подключения к $DB_HOST:$DB_PORT...';
        sleep 2; 
    done
" || {
    echo "Не удалось подключиться к PostgreSQL по адресу $DB_HOST:$DB_PORT!"
    echo "Проверьте:"
    echo "1. Что сервис PostgreSQL запущен"
    echo "2. Что хост и порт указаны правильно"
    echo "3. Что нет проблем с сетью/файрволлом"
    echo "4. Что ваш контейнер имеет доступ к внутренней сети Render"
    exit 1
}

# Проверяем возможность подключения через psql
echo "Проверка аутентификации в PostgreSQL..."
timeout 30 psql "$DATABASE_URL" -c '\q' || {
    echo "Не удалось аутентифицироваться в PostgreSQL!"
    echo "Проверьте правильность учетных данных в DATABASE_URL"
    exit 1
}
echo "PostgreSQL готов и доступен!"

cd src || true

echo "Применение миграций..."
python manage.py migrate

echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создаем суперпользователя только если не в production или для теста
if [ "$DJANGO_ENV" != "production" ]; then
    echo "Создание суперпользователя..."
    python manage.py createsuperuser --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --password "$DJANGO_SUPERUSER_PASSWORD" || \
    echo "Суперпользователь уже существует или произошла ошибка"
fi

echo "Запуск Gunicorn..."
exec gunicorn medbook.wsgi:application --bind 0.0.0.0:"${PORT:-8000}" --workers 2 --timeout 120


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