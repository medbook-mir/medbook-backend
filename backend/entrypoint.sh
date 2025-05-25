#!/bin/bash
set -e

echo "=== Starting Initialization ==="
echo "🔍 Environment: $DJANGO_SETTINGS_MODULE"
echo "📦 Database: ${DATABASE_URL//:[^@]*@/:<hidden>@}"

if [[ ! "$DATABASE_URL" =~ ^postgres(ql)?:// ]]; then
    echo "❌ Error: Invalid DATABASE_URL format. Must start with postgres:// or postgresql://"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo "Installing postgresql-client..."
    apt-get update && apt-get install -y postgresql-client
fi

max_attempts=2
attempt=1
connected=false

while [ $attempt -le $max_attempts ]; do
    if psql "$DATABASE_URL" -c '\q' 2>/dev/null; then
        connected=true
        break
    fi
    echo "⏳ Attempt $attempt/$max_attempts - Waiting for PostgreSQL..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ "$connected" = false ]; then
    echo "❌ Failed to connect to PostgreSQL after $max_attempts attempts!"
    exit 1
fi

echo "✅ PostgreSQL connection established!"

cd src
echo "🔄 Applying migrations..."
python manage.py migrate

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "👑 Checking superuser..."
if ! python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(is_superuser=True, is_active=True).exists())
" | grep -q "True"; then
    echo "👑 No active superuser found, creating one..."
    export DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" 2>/dev/null || \
    echo "❌ Failed to create superuser (check logs for details)"
else
    echo "ℹ Active superuser already exists, skipping creation"
fi


echo "🚀 Starting Gunicorn..."
exec gunicorn medbook.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 20 \
    --access-logfile -