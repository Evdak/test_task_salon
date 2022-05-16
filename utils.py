from datetime import datetime, timedelta, time
import uuid
import pytz
from config import *
utc = pytz.UTC
UUID_ID = uuid.UUID


def check_timedelta_before(time: datetime = datetime.now(tz=utc)) -> datetime:
    return time - timedelta(minutes=DEFAULT_TIME)


def check_timedelta_after(time: datetime = datetime.now(tz=utc)) -> datetime:
    return time + timedelta(minutes=DEFAULT_TIME)


def get_open_datetime() -> datetime:
    open_time = OPEN_TIME.split(':')
    open_time = list(map(int, open_time))
    return datetime.combine(date=datetime.now().date(), time=time(
        hour=open_time[0], minute=open_time[1]), tzinfo=utc).time()


def get_close_datetime() -> datetime:
    close_time = CLOSE_TIME.split(':')
    close_time = list(map(int, close_time))
    return datetime.combine(date=datetime.now().date(), time=time(
        hour=close_time[0], minute=close_time[1]), tzinfo=utc).time()


def get_close_datetime_full() -> datetime:
    close_time = CLOSE_TIME.split(':')
    close_time = list(map(int, close_time))
    return datetime.combine(date=datetime.now().date(), time=time(
        hour=close_time[0], minute=close_time[1]), tzinfo=utc).time()


def get_live_queue_max_count() -> int:
    result = get_close_datetime_full() - datetime.now(tz=utc)
    return int(result.seconds/(DEFAULT_TIME*60))
