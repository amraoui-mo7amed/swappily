FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

# CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && daphne -b 0.0.0.0 -p $PORT core.asgi:application"]
CMD ["sh", "-c", "\
    python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py migrate --run-syncdb && \
    DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin} \
    DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com} \
    DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} \
    python manage.py createsuperuser --noinput 2>/dev/null || true && \
    daphne -b 0.0.0.0 -p $PORT core.asgi:application \
"]