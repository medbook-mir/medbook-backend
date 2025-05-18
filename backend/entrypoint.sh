#!/bin/bash
set -e  

echo "DATABASE_URL: ${DATABASE_URL//:[^@]*@/:<hidden>@}"


echo "Ожидание PostgreSQL..."
timeout 60 sh -c "until psql \"$DATABASE_URL\" -c '\q' 2>/dev/null; do sleep 2; done" || {
    echo "Не удалось подключиться к PostgreSQL!"
    exit 1
}
echo "PostgreSQL готов!"


cd src || true

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" --password "$DJANGO_SUPERUSER_PASSWORD" || true


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