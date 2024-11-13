python manage.py runserver
celery -A geheimvz worker -l INFO
docker run --rm -p 5672:5672 rabbitmq:3-alpine
