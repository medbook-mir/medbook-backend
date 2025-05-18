#!/bin/bash
apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*


echo "Проверка разрешения имени хоста..."
nslookup dpg-d0kap7je5dua73bk1vg0-a.frankfurt-postgres.render.com


echo "Ожидание PostgreSQL ($POSTGRES_HOST)..."
timeout 30 sh -c "until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB; do sleep 2; done" || {
    echo "Не удалось подключиться к PostgreSQL!"
    exit 1
}


python manage.py migrate
python manage.py collectstatic --noinput


exec gunicorn medbook.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120


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