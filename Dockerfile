# Используем официальный Python образ в качестве базового
FROM python:3.10.2-slim

RUN apt-get update && apt-get install -y git

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./PhotoShare ./PhotoShare
COPY ./migration ./migration
COPY requirements.txt ./
COPY .env ./
COPY alembic.ini ./
COPY run_uvicorn.sh ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Делаем скрипт исполняемым
RUN chmod +x run_uvicorn.sh

# Указываем команду для запуска приложения
CMD ["./run_uvicorn.sh"]


