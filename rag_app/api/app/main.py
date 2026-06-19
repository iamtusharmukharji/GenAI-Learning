from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse   
from typing import Optional
from rq_conf import rq_client

app = FastAPI(
    title="RAG App",
    description="A simple RAG app powered by FastAPI",
    version="0.1.0",
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
async def read_root():
    return RedirectResponse('/docs')

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post('/chat')
async def chat(
    query :str
):  
    job_id = rq_client.rq.enqueue(rq_client.process_query, query)
    return {"status":"success", "job_id":job_id.id, "message":"queued"}

@app.get('/job-status')
async def job_status(
    job_id :str
):  
    job = rq_client.rq.fetch_job(job_id= job_id)
    res = job.return_value()
    stat = job.get_status()
    return {"status":stat,"result":res}
