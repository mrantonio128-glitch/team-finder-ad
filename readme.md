# TeamFinder (вариант 1)

python = 3.14
django==6.0.6
pillow==12.2.0
psycopg[binary]==3.3.4
python-decouple==3.8

## Подготовка к запуску
Создать файл `.env` со следующим содержимым:
```dotenv
DJANGO_SECRET_KEY=secret_key_for_you
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web,0.0.0.0

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=db
POSTGRES_PORT=5432

## Запуск
```bash
#билд, миграции выполняются сами в docker-entrypoint.sh
docker compose up --build -d
#заполнение данными
docker compose exec web python manage.py seed_db
```
Адресс для проверки проекта http://localhost:8000/

