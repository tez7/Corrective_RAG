from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

CHROMA_PATH = "chroma_db"

EMBED_MODEL = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

LLM = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)