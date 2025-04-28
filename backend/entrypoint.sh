#!/bin/bash
if ! curl -s http://localhost:8000/health-check/ >/dev/null; then
  echo "🔄 Запуск Django..."
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
else
  echo "✅ Django уже запущен"
fi