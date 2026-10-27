FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    locales \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY . .
# RUN python manage.py collectstatic --noinput
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

# CMD ["sh", "-c", "python manage.py migrate && gunicorn medbook.wsgi:application --bind 0.0.0.0:$PORT --timeout 120"
CMD ["sh", "-c", "sleep 10 && python manage.py check_db_connection && gunicorn medbook.wsgi:application --bind 0.0.0.0:$PORT"]