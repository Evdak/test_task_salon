import os

try:
    DEFAULT_TIME = os.getenv('DEFAULT_TIME')
    OPEN_TIME = os.getenv('OPEN_TIME')
    CLOSE_TIME = os.getenv('CLOSE_TIME')
    NAME = os.getenv('NAME')
    DESTINATION = os.getenv('DESTINATION')
    PHONE_NUMBER = os.getenv('PHONE_NUMBER')
    BASE_URL = os.getenv('BASE_URL')
except:
    DEFAULT_TIME = 30
    OPEN_TIME = "8:00"
    CLOSE_TIME = "22:00"
    NAME = "Barbershop"
    DESTINATION = "Казань, ул. Баумана, д.1"
    PHONE_NUMBER = "+79999999999"
    BASE_URL = "sqlite+aiosqlite:///./test.db"
