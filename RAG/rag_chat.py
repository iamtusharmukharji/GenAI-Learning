from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from cred_loader import creds

ai_client = OpenAI(
    api_key=creds.api_key["GEMNI_API_KEY"],
    base_url=creds.api_key["GEMNI_API_URL"]
)

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding= embedding_model,
    url= "http://localhost:6333",
    collection_name="rag_collection"
)

# take user input

qry = input("Ask anything >>> ")

# perform similarity search
search_res = vector_db.similarity_search(query = qry)


# Prepare LLM call

SYS = f"""
    You are an assistant that responds user query related to
    some internal document with the context data provided below

    Context : {search_res}
"""
chat = ai_client.chat.completions.create(
    model = "gemini-2.5-flash-lite",
    # response_format= LLMOutputSchema,
    messages = [
        {"role":"system","content":SYS},
        {"role":"user","content":qry}
    ] 
)

print(chat.choices[0].message.content)

