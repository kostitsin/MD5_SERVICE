## MD5 Service

Веб-сервис, позволяющий посчитать MD5-хеш от файла, расположенного в сети Интернет.

## Запуск проекта

**Для того, чтобы запустить программу на своём компьютере, необходимо:**

1. Склонировать репозиторий с GitHub. 

`https://github.com/kostitsin/MD5_service.git`

2. Установить MongoDB. 

	1. Установка mongo

	`brew install mongodb`

	2. Запуск MongoDB. 

	`mongo`

	3. Создание базы данных MD5_db. 

	`use MD5_db`

3. Установить Redis, запустить Redis-сервер. 

`brew install redis`. 

`brew services start redis`

4. Перейти в папку с проектом. 

`cd MD5_service/server`

5. Установить виртуальное окружение. 

	1. Установка инструмента virtualenv. 

	`pip install virtualenv`

	2. Создание новой виртуальной среды. 

	`python3 -m venv env`

	3. Активация. 

	`source env/bin/activate`

6. Установить зависимости. 

`pip install -r requirements.txt`

7. Запустить Celery. 

`celery -A flaskserv.celery  worker --loglevel=info`

8. Запустить сервер. 

`FLASK_APP=flaskserv.py flask run`

Чтобы потом вернуться из env в контекст system. 

`deactivate`

Celery и Flask запускаются с разных терминалов, в каждом нужно войти в окружение

Инструкция написана под macOS

Для работы функции отправки почты необходимо в файле send_mail.py вписать адрес электронной почты и пароль от неё

## Пример использования

`curl -X POST -d "email=user@example.com&url=http://site.com/file.txt" http://localhost:8000/submit`

{"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}

`curl -X GET http://localhost:8000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac`

{"status":"running"}

`curl -X GET http://localhost:8000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac`

{"md5":"f4afe93ad799484b1d512cc20e93efd1","status":"done","url":" http://site.com/file.txt"}