# Используйте базовый образ Python
FROM python:3.9

# Установите рабочую директорию
WORKDIR /app

# Скопируйте requirements.txt и установите зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Скопируйте исходный код проекта
COPY . .

# Определите порт, который будет прослушивать ваше приложение
EXPOSE 8000

# Запустите приложение
CMD python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input && python manage.py loaddata test_data.json && python manage.py runserver 0.0.0.0:8000