# Реалізація проекту

Для роботи проекта необхідний файл `.env` зі змінними оточення.
Створіть його з таким вмістом і підставте свої значення.

```dotenv

# Database PostgreSQL
SQLALCHEMY_DATABASE_URL=postgresql://username:password@localhost:5433/postgres
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=

# JWT authentication
SECRET_KEY=
ALGORITHM=

# Email service
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

# Redis
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
```

Запуск баз даних


```bash
docker-compose up --build
```

Міграця баз даних


```bash
alembic upgrade head
```

Запуск застосунку


```bash
uvicorn PhotoShare.main:app
```