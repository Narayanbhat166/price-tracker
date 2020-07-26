from redis import Redis
from rq import Queue
import datetime
import pytz
import random

from models import Flipkart, Amazon, User

from redis_functions.redis_amazon import update_amazon
from redis_functions.redis_flipkart import update_flipkart


class Time:
    def __init__(self):
        self.last_time = datetime.datetime.now(
            tz=pytz.timezone('Asia/Kolkata'))

    def get_time(self):
        random_seconds = random.randint(1, 4)
        print("Random seconds: ", random_seconds)
        Timedelta = datetime.timedelta(seconds=random_seconds)
        new_time = self.last_time + Timedelta
        self.last_time = new_time
        print("Job scheduled at: ", new_time)

        return new_time


def update_db():
    redis_connection = Redis(host="pearlfish.redistogo.com", port=10453,
                             password="6b7025eac8f3f18072d7496c96d8e8c5", username="redistogo")
    q = Queue('test_queue', connection=redis_connection)

    time = Time()

    products = Amazon.query.all()

    for product in products:
        product_id = product.product_id

        job = q.enqueue_at(time.get_time(), update_amazon, product_id)
        print("Created Amazon Job: ", job.id)

    products = Flipkart.query.all()

    for product in products:
        product_id = product.product_id

        job = q.enqueue_at(time.get_time(), update_flipkart, product_id)
        print("Created Flipkart Job: ", job.id)
