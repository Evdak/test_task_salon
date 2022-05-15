import os

try:
    DEFAULT_TIME = os.environ['DEFAULT_TIME']
    OPEN_TIME = os.environ['OPEN_TIME']
    CLOSE_TIME = os.environ['CLOSE_TIME']
    NAME = os.environ['NAME']
    DESTINATION = os.environ['DESTINATION']
    PHONE_NUMBER = os.environ['PHONE_NUMBER']
    BASE_URL = os.environ['BASE_URL']
except:
    DEFAULT_TIME = 30
    OPEN_TIME = "8:00"
    CLOSE_TIME = "22:00"
    NAME = "Barbershop"
    DESTINATION = "Казань, ул. Баумана, д.1"
    PHONE_NUMBER = "+79999999999"
    BASE_URL = "sqlite+aiosqlite:///./test.db"
