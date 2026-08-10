# Django API для курсов и уроков

Проект на Django + Django REST Framework.

## Возможности

- Кастомная модель пользователя (авторизация по email, телефон, город, аватарка)
- Модели `Course` и `Lesson` (связь один-ко-многим)
- CRUD для курсов через `ViewSet`
- CRUD для уроков через Generic-классы
- Редактирование профиля любого пользователя

## Установка

```bash
pip install django djangorestframework Pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Эндпойнты
Курсы
GET	/courses/
POST	/courses/
GET	/courses/{id}/
PATCH	/courses/{id}/
DELETE	/courses/{id}/

Уроки
Метод	URL
GET	/lessons/
POST	/lessons/
GET	/lessons/{id}/
PATCH	/lessons/{id}/
DELETE	/lessons/{id}/

Пользователи
Метод	URL
GET	/users/{id}/
PATCH	/users/{id}/

Примечание
Авторизация пока не подключена — все эндпоинты открыты.
