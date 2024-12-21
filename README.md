```
docker run --rm -v geheimvz_db:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=geheimvz postgres:17-alpine
docker run --rm -p 6379:6379 redis:7-alpine

python manage.py runserver
python manage.py rundramatiq
```
