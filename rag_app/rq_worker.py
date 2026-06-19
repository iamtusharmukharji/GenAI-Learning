from redis import Redis
from rq import Queue
from rq.worker import SimpleWorker

# if using standalone we will us localhost but when runnig inside container
# localhost becomes redis(service name)
redis_conn = Redis(host="localhost", port=6379)

queue = Queue(connection=redis_conn)

worker = SimpleWorker([queue], connection=redis_conn)

worker.work()