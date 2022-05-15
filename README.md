# test_task_salon
Для запуска проекта используйте эти команды (из корневой папки проекта):

Информационные данные (можно заменить):
<br>
`echo DEFAULT_TIME=30 >.env`
<br>
` echo OPEN_TIME="8:00" >.env`
<br>
` echo CLOSE_TIME="22:00" >.env`
<br>
` echo NAME="Barbershop" >.env`
<br>
` echo DESTINATION="Казань, ул. Баумана, д.1" >.env`
<br>
` echo PHONE_NUMBER="+79999999999" >.en`
<br>
` echo BASE_URL="sqlite+aiosqlite:///./test.db" >.env`



Если не установлен pipenv:
<br>
`pip3 install pipenv`

Для запуска:
<br>
`pipenv shell`
<br>
`pipenv install`
<br>
`python3 main.py`

Сервер запущен по адресу: http://127.0.0.1:8000
<br>
http://127.0.0.1:8000/docs - документация

Допущения:
<br>
В переменнуб `DEFAULT_TIME` записано время выделямое на человека в минутах
