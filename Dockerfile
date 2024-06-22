# Використовуємо офіційний образ Python версії 3.11
FROM python:3.10.2-slim

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копіюємо файли залежностей у контейнер
COPY requirements.txt .

# Встановлюємо залежності за допомогою pip
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь вміст поточної директорії у контейнер у /app
COPY . .
