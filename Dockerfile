FROM python:3.11

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Ensure the database file is in a persistent location
ENV SQLITE_DB_PATH=/app/data/db.sqlite3

CMD ["sh", "-c", "\
    python manage.py collectstatic --noinput && \
    python manage.py migrate --run-syncdb && \
    python manage.py migrate && \
    DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin} \
    DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com} \
    DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin} \
    python manage.py createsuperuser --noinput 2>/dev/null || true && \
    daphne -b 0.0.0.0 -p $PORT core.asgi:application \
"]