# Описание
__Приложение для бронирования комнат в отеле.__
## Функционал
```
* Пользователи могут фильтровать и сортировать комнаты по цене, по количеству мест.
* Пользователи могут получить список свободных комнаты.
* Пользователи могут бронировать свободную комнату.
* Суперюзер может добавлять/удалять/редактировать комнаты и редактировать записи о бронях через админ-панель Django.
* Брони могут быть отменены как самим юзером, так и суперюзером.
* Пользователи умееют регистрироваться и авторизовываться (логиниться).
```
## Права доступа
```
* Неавторизованный пользователь
    * Получение списка всех комнат
    * Получение списка свобоных комнат
    * Получение информацию о конкретной комнате
* Авторизованный пользователь
    * Получение списка всех комнат
    * Получение списка свобоных комнат
    * Получение информацию о конкретной комнате
    * Получение списка своих броней
    * Создание брони комнаты
    * Удаление __своей__ брони комнаты
* Суперпользователь
    * Получение списка всех комнат
    * Получение списка свобоных комнат
    * Получение информацию о конкретной комнате
    * Получение списка своих броней
    * Создание брони комнаты
    * Удаление __любой__ брони комнаты
    * Создание комнаты
    * Удаление комнаты
```
## Подготовка и запуск проекта
#### Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone git@github.com:Slavchick12/hotel.git
```
#### Настройка виртуального окружения
#####Шаг 1. Установка виртуального окружения
```bash
cd hotel/
```
```bash
python -m venv venv
```
#####Шаг 2. Активация виртуального окружения
```bash
python -m pip instal
```
#####Шаг 3. Обновление пакетов pip
```bash
python -m pip install -U pip
```
#####Шаг 4. Установка зависимостей проекта
```bash
pip install -r requirements.txt
```
#### Подготовка базы данных PostgreSQL
#####Шаг 1. Скачайте и установите PostreSQL 14.5
```
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
```
#####Шаг 2. Перейдите в директорию с файлом manage.py с запущенным виртуальным окружением
```bash
cd <path_to_project>/hotel/backend/hotel/
```
#####Шаг 3. Проведите миграции
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
#### Запуск проекта на локальной машине
```bash
python manage.py runserver
```
#### Создание суперюзера
```bash
python manage.py createsuperuser
```
#### Админ-панель Django
```bash
http://127.0.0.1:8000/admin
```
## Используемый стек
```
Django, DRF, PostgreSQL, Simple-JWT
```
#### Также используется
```
flake8, isort, django-filter, psycopg2-binary
```