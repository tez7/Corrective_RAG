from langchain_chroma import Chroma
from langchain_core.documents import Document

from ingestion.embedder import get_embedding_model
from ingestion.config import CHROMA_PATH


# -----------------------------------
# STORE CHUNKS
# -----------------------------------

def store_chunks(documents):

    print(
        f"\nStoring {len(documents)} chunks "
        f"into ChromaDB..."
    )

    vectordb = Chroma.from_documents(

        documents=documents,

        embedding=get_embedding_model(),

        persist_directory=CHROMA_PATH
    )

    print("\nVector Storage Completed")

    return vectordb