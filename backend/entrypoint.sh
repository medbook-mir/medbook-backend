#!/bin/bash
set -e

echo "=== Starting Initialization ==="
echo "DATABASE_URL: ${DATABASE_URL//:[^@]*@/:<hidden>@}"

if [[ ! "$DATABASE_URL" =~ ^postgres(ql)?:// ]]; then
    echo "❌ Error: Invalid DATABASE_URL format. Must start with postgres:// or postgresql://"
    exit 1
fi

echo "🔍 Testing PostgreSQL connection..."

DB_HOST=$(echo $DATABASE_URL | cut -d@ -f2 | cut -d: -f1)
DB_PORT=5432

if ! command -v psql &> /dev/null; then
    echo "Installing postgresql-client..."
    apt-get update && apt-get install -y postgresql-client
fi

max_attempts=30
attempt=1
connected=false

while [ $attempt -le $max_attempts ]; do
    if psql "$DATABASE_URL" -c '\q' 2>/dev/null; then
        connected=true
        break
    fi
    
    echo "⏳ Attempt $attempt/$max_attempts - Waiting for PostgreSQL..."
    sleep 2
    attempt=$((attempt + 1))
done

if [ "$connected" = false ]; then
    echo "❌ Failed to connect to PostgreSQL after $max_attempts attempts!"
    echo "Troubleshooting steps:"
    echo "1. Verify PostgreSQL service is running in Render dashboard"
    echo "2. Check the 'Links' section in your web service settings"
    echo "3. Try recreating the PostgreSQL service"
    echo "4. Contact Render support with these logs"
    exit 1
fi

echo "✅ PostgreSQL connection established!"


cd src

echo "🔄 Applying migrations..."
python manage.py migrate

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" != "production" ]; then
    echo "👑 Creating superuser..."
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --password "$DJANGO_SUPERUSER_PASSWORD" 2>/dev/null || \
    echo "ℹ Superuser already exists or error occurred"
fi

echo "🚀 Starting Gunicorn..."
exec gunicorn medbook.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile -
