# 📖 Web-library Django
Pet-project, создаваемый в целях изучения фреймворка Django

## Стек проекта: 
- Python 3.12
- Django 5.1 (Django REST framework)
- HTML5, CSS, JS 
- PostgreSQL 17.0
- Docker 27.4.0
- Celery, Redis

## Установка и запуск:

1.  Склонируйте репозиторий:
    ```bash
    git clone <my_repository_url>
    cd <your_directory>
    ```

2.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # для macOS/Linux
    venv\Scripts\activate # для Windows
    ```

3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4.  Настройте переменные окружения:
    ```
    Добавьте свои переменные в файл .env.
    ```    

5.  Примените миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  Запустите сервер:
    ```bash
    python manage.py runserver
    ``` 
    
## Docker:
- Сборка контейнера и приняте миграций:
    ```bash
    docker-compose up --build

    docker-compose exec weblibrary python manage.py migrate
    ```
- Остановка контейнера:
    ```bash
    docker-compose down
    ```
- Удаление контейнера:
    ```bash
    docker rm -f <container_name_or_id>
    ```

## Админка:
```bash
python manage.py createsuperuser --username <your_superuser_name>
```

## API:
- Получение ключей:
    ```bash
    https://.../token?username='your_username'&password='your_password'
    ```
    Будет получено два токена acsess и refresh

- Использование токена:
    ```bash
    https://.../api/books?authorization='Bearer <your_accesstoken>'
    ```
    
- Обновление токена:
    ```bash
    https://.../token/refresh/?refresh='your_refreshtoken'
    ```

## Скрины:
Главная страница
![Главаная страница](https://github.com/Gewfreee/Django-pet-project/blob/main/images/Снимок%20экрана%202025-01-16%20024021.png)

Профиль
![Профиль](https://github.com/Gewfreee/Django-pet-project/blob/main/images/Снимок%20экрана%202025-01-21%20005435.png)
