#!/bin/bash
set -e  

echo "DATABASE_URL: ${DATABASE_URL//:[^@]*@/:<hidden>@}"


if [ -z "$DATABASE_URL" ]; then
    echo "Ошибка: DATABASE_URL не установлена!"
    exit 1
fi

DB_HOST=$(echo $DATABASE_URL | awk -F[@] '{print $2}' | awk -F[:/] '{print $1}')

echo "Ожидание PostgreSQL ($DB_HOST)..."

timeout 120 sh -c "while ! nc -z $DB_HOST 5432; do sleep 2; done" || {
    echo "Не удалось подключиться к PostgreSQL по адресу $DB_HOST:5432!"
    echo "Проверьте:"
    echo "1. Что сервис PostgreSQL запущен"
    echo "2. Что хост и порт указаны правильно"
    echo "3. Что нет проблем с сетью/файрволлом"
    exit 1
}


timeout 30 psql "$DATABASE_URL" -c '\q' || {
    echo "Не удалось аутентифицироваться в PostgreSQL!"
    exit 1
}
echo "PostgreSQL готов!"

cd src || true

python manage.py migrate
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" != "production" ]; then
    python manage.py createsuperuser --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --password "$DJANGO_SUPERUSER_PASSWORD" || true
fi

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