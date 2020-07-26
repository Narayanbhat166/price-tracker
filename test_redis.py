from redis import Redis
from rq import Queue
import datetime
import pytz
import random

from redis_functions.redis_updater import update_db


redis_connection_local = Redis(host="pearlfish.redistogo.com", port=10453,
                               password="6b7025eac8f3f18072d7496c96d8e8c5", username="redistogo")


q = Queue('test_queue', connection=redis_connection_local)


# class Time:
#     def __init__(self):
#         self.last_time = datetime.datetime.now(
#             tz=pytz.timezone('Asia/Kolkata'))

#     def get_time(self):
#         random_seconds = random.randint(1, 5)
#         print("Random seconds: ", random_seconds)
#         Timedelta = datetime.timedelta(seconds=random_seconds)
#         new_time = self.last_time + Timedelta
#         self.last_time = new_time
#         print("Job scheduled at: ", new_time)

#         return new_time


# enqueue 10 jobs to run at time intervals of 1 minute
present_time = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'))

for i in range(0, 10):
    new_time = present_time + datetime.timedelta(minutes=1)
    present_time = new_time
    job = q.enqueue_at(new_time, update_db)
    print(job)


# naive datetime
# timef = datetime.datetime.combine(datetime.date.today(), datetime.time(12, 11))
# timea = datetime.datetime.combine(datetime.date.today(), datetime.time(12, 12))

# timezone_awaredatetime
# timezone_india = pytz.timezone('Asia/Kolkata')


# time = datetime.time(12, 30)
# date_time = datetime.datetime.now(timezone)
# timedelta = datetime.timedelta(seconds=random_seconds)

# dt = date_time + timedelta
# this is a naive datetime, convert it to timezone aware datetime


# new_dt = timezone_india.localize(dt)

# joba = q.enqueue_at(time.get_time(), amazon, amazon_productid)
# jobf = q.enqueue_at(time.get_time(), flipkart, flipkart_productid)
