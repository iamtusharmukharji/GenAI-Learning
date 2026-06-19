from redis import Redis
from rq import Queue
from openai import OpenAI
import cred_loader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
# from tasks import send_email

conn = Redis(
    host="localhost",
    port="6379"
) 

rq = Queue(
    connection= conn
)

cred = cred_loader.creds

def process_query(query_str):

    client = OpenAI(
        api_key= cred.api_key['GEMNI_API_KEY'],
        base_url= cred.api_key['GEMNI_API_URL']
    )

    # perform similarity search    
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_db = QdrantVectorStore.from_existing_collection(
        embedding= embedding_model,
        url= "http://localhost:6333",
        collection_name="rag_collection"
    )

    context = vector_db.similarity_search(query= query_str)

    SYS = f"""
            You are an assistant that responds user query related to
            some internal document with the context data provided below

            Context : {context}
    """

    chat = client.chat.completions.create(
        model = "gemini-2.5-flash-lite",
        # response_format= LLMOutputSchema,
        messages = [
            {"role":"system","content":SYS},
            {"role":"user","content":query_str}
        ] 
    )

    return chat.choices[0].message.content




# rq.enqueue(send_email, "abc@gmail.com")