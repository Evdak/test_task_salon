# test_task_salon
Для запуска проекта используйте эти команды (из корневой папки проекта):

Информационные данные (можно заменить):
<br>
`echo 'DEFAULT_TIME=30`
<br>
`OPEN_TIME="8:00"`
<br>
`CLOSE_TIME="22:00"`
<br>
`NAME="Barbershop"`
<br>
`DESTINATION="Казань, ул. Баумана, д.1"`
<br>
`PHONE_NUMBER="+79999999999"`
<br>
`BASE_URL="sqlite+aiosqlite:///./test.db"' >.env`


echo 'DEFAULT_TIME=30 
OPEN_TIME="8:00"
CLOSE_TIME="22:00"
NAME="Barbershop"
DESTINATION="Казань, ул. Баумана, д.1"
PHONE_NUMBER="+79999999999"
BASE_URL="sqlite+aiosqlite:///./test.db" ' >.env

Если не установлен pipenv:
<br>
`pip3 install pipenv`

Для запуска:
<br>
`pipenv shell`
<br>
`pipenv install`
<br>
`pipenv run python3 main.py`

Сервер запущен по адресу: http://127.0.0.1:8000
<br>
http://127.0.0.1:8000/docs - документация

Допущения:
<br>
В переменную `DEFAULT_TIME` записано время выделямое на человека в минутах
