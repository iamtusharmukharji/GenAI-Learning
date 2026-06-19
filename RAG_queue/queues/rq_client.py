from redis import Redis
from rq import Queue
from tasks import send_email

conn = Redis(
    host="localhost",
    port="6379"
) 

rq = Queue(
    connection= conn
)


rq.enqueue(send_email, "abc@gmail.com")