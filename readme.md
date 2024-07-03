# PhotoShare a web service

To run the project, you need an ```.env``` file with environment variables. Create it with the following content and replace 
with your own values.

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

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Veslo7601/Python_Web_Project.git
```

2. Create a virtual environment (recommended) and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies using requirements.txt:

```bash
pip install -r requirements.txt
```

### **Add ```.env``` file**

4. Set up the database:

```bash
docker compose up
alembic upgrade head
```

5. Run the application:

```bash
uvicorn PhotoShare.main:app
```