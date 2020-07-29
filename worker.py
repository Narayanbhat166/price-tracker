from redis import Redis
from rq import Worker, Queue

redis_connection_local = Redis(host="pearlfish.redistogo.com", port=10453,
                               password="6b7025eac8f3f18072d7496c96d8e8c5", username="redistogo")


q = Queue('scrapper', connection=redis_connection_local)

worker = Worker(q, connection=redis_connection_local)

worker.work(with_scheduler=True)
print("Worker running")
