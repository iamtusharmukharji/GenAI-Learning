from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

# Loading Phase

pdf_path = Path(__file__).parent / "arduHandbook.pdf"

loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()

page_num = 12

# print(docs[page_num])

# Chunking Phase

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

chunks = text_splitter.split_documents(documents = docs)

# Vector Embeddings

# embedding_model = GoogleGenerativeAIEmbeddings(
#     model= "models/gemini-embedding-001",
#     google_api_key="AIzaSyAqhsVgw0QiOD8tjLHW7dj9HRyYbg2BpPQ"
# )

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vector_store = QdrantVectorStore.from_documents(
    documents= chunks,
    embedding= embedding_model,
    url = "http://localhost:6333",
    collection_name = "rag_collection"
)

