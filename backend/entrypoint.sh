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

if [[ "$TESTING" != "true" ]]; then
    if [[ "$DJANGO_SETTINGS_MODULE" == "medbook.settings.local" ]]; then
        if [[ "$SERVICE_TYPE" == "backend" ]]; then
            echo "🔄 [LOCAL-BACKEND] Applying migrations..."
            python manage.py migrate
            
            echo "🔄 [LOCAL-BACKEND] Creating initial fixtures..."
            python manage.py loaddata fixtures/initial_data.json

            echo "📦 [LOCAL-BACKEND] Collecting static files..."
            python manage.py collectstatic --noinput

            echo "👑 [LOCAL-BACKEND] Checking superuser..."
            if ! python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(is_superuser=True, is_active=True).exists())
" | grep -q "True"; then
                echo "👑 [LOCAL-BACKEND] No active superuser found, creating one..."
                export DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
                python manage.py createsuperuser \
                    --noinput \
                    --username "$DJANGO_SUPERUSER_USERNAME" 2>/dev/null || \
                echo "❌ [LOCAL-BACKEND] Failed to create superuser (check logs for details)"
            else
                echo "ℹ [LOCAL-BACKEND] Active superuser already exists, skipping creation"
            fi
        elif [[ "$SERVICE_TYPE" == "api" ]]; then
            echo "ℹ [LOCAL-API] Skipping migrations (handled by backend service)"
            echo "📦 [LOCAL-API] Collecting static files..."
            python manage.py collectstatic --noinput
        else
            echo "⚠ [LOCAL] Unknown SERVICE_TYPE: $SERVICE_TYPE - skipping migration and superuser setup"
        fi
    elif [[ "$DJANGO_SETTINGS_MODULE" == "medbook.settings.prod" ]]; then
        if [[ "$SERVICE_TYPE" == "api" ]]; then
            echo "🔄 [PROD-API] Applying migrations..."
            python manage.py migrate

            echo "🔄 [PROD-API] Creating initial fixtures..."
            python manage.py loaddata fixtures/initial_data.json

            echo "📦 [PROD-API] Collecting static files..."
            python manage.py collectstatic --noinput

            echo "👑 [PROD-API] Checking superuser..."
            if ! python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(is_superuser=True, is_active=True).exists())
" | grep -q "True"; then
                echo "👑 [PROD-API] No active superuser found, creating one..."
                export DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
                python manage.py createsuperuser \
                    --noinput \
                    --username "$DJANGO_SUPERUSER_USERNAME" 2>/dev/null || \
                echo "❌ [PROD-API] Failed to create superuser (check logs for details)"
            else
                echo "ℹ [PROD-API] Active superuser already exists, skipping creation"
            fi
        elif [[ "$SERVICE_TYPE" == "backend" ]]; then
            echo "ℹ [PROD-BACKEND] Skipping migrations (handled by api service)"
            echo "📦 [PROD-BACKEND] Collecting static files..."
            python manage.py collectstatic --noinput
        else
            echo "⚠ [PROD] Unknown SERVICE_TYPE: $SERVICE_TYPE - skipping migration and superuser setup"
        fi
    else
        echo "⚠ Unknown environment: $DJANGO_SETTINGS_MODULE - skipping migration and superuser setup"
    fi
else
    echo "⚠ Skipping migration and superuser setup (TESTING=$TESTING)"
fi

echo "🚀 Starting Gunicorn..."
exec gunicorn medbook.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 20 \
    --access-logfile - \
    --reload
