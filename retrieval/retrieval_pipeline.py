from collections import defaultdict

from rank_bm25 import BM25Okapi

from langchain_chroma import Chroma
from langchain_core.documents import Document

from ingestion.config import CHROMA_PATH
from ingestion.embedder import get_embedding_model

from retrieval.utils import (
    deduplicate_chunks,
    print_chunks
)


# -----------------------------
# LOAD VECTOR DB
# -----------------------------

vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=get_embedding_model()
)


# -----------------------------
# DENSE RETRIEVAL
# -----------------------------

def dense_retrieval(query, k=10):

    retriever = vectordb.as_retriever(
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    return docs


# -----------------------------
# BM25 RETRIEVAL
# -----------------------------

def bm25_retrieval(query, k=10):

    collection = vectordb.get()

    texts = collection["documents"]

    metadatas = collection["metadatas"]

    tokenized_docs = [
        text.split()
        for text in texts
    ]

    bm25 = BM25Okapi(tokenized_docs)

    scores = bm25.get_scores(
        query.split()
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    documents = []

    for idx in ranked_indices:

        documents.append(
            Document(
                page_content=texts[idx],
                metadata=metadatas[idx]
            )
        )

    return documents


# -----------------------------
# RECIPROCAL RANK FUSION
# -----------------------------

def reciprocal_rank_fusion(
    dense_docs,
    bm25_docs,
    k=60
):

    scores = defaultdict(float)

    all_docs = {}

    # Dense Scores
    for rank, doc in enumerate(dense_docs):

        doc_id = doc.page_content[:100]

        scores[doc_id] += 1 / (k + rank)

        all_docs[doc_id] = doc

    # BM25 Scores
    for rank, doc in enumerate(bm25_docs):

        doc_id = doc.page_content[:100]

        scores[doc_id] += 1 / (k + rank)

        all_docs[doc_id] = doc

    sorted_docs = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    fused_docs = [
        all_docs[doc_id]
        for doc_id, _ in sorted_docs
    ]

    return fused_docs


# -----------------------------
# CHUNK REORDERING
# -----------------------------

def reorder_chunks(documents):

    """
    Lost-in-the-middle mitigation.

    Put strongest chunks
    at beginning and end.
    """

    if len(documents) <= 2:
        return documents

    reordered = []

    reordered.append(documents[0])

    reordered.extend(documents[2:])

    reordered.append(documents[1])

    return reordered


# -----------------------------
# MAIN HYBRID RETRIEVAL
# -----------------------------

def hybrid_retrieval(
    query,
    top_k=10
):

    # -------------------------
    # DENSE SEARCH
    # -------------------------

    print("\nRunning Dense Retrieval...")

    dense_docs = dense_retrieval(
        query=query,
        k=top_k
    )

    print(f"Dense Retrieved: {len(dense_docs)}")


    # -------------------------
    # BM25 SEARCH
    # -------------------------

    print("\nRunning BM25 Retrieval...")

    bm25_docs = bm25_retrieval(
        query=query,
        k=top_k
    )

    print(f"BM25 Retrieved: {len(bm25_docs)}")


    # -------------------------
    # HYBRID FUSION
    # -------------------------

    print("\nApplying Reciprocal Rank Fusion...")

    fused_docs = reciprocal_rank_fusion(
        dense_docs,
        bm25_docs
    )

    print(f"After Fusion: {len(fused_docs)}")


    # -------------------------
    # DEDUPLICATION
    # -------------------------

    print("\nRemoving Duplicate Chunks...")

    fused_docs = deduplicate_chunks(
        fused_docs
    )

    print(f"After Deduplication: {len(fused_docs)}")


    # -------------------------
    # CHUNK REORDERING
    # -------------------------

    print("\nReordering Chunks...")

    final_docs = reorder_chunks(
        fused_docs
    )


    # -------------------------
    # FINAL TOP K
    # -------------------------

    final_docs = final_docs[:top_k]


    # -------------------------
    # PRINT CHUNKS
    # -------------------------

    print_chunks(final_docs)

    return final_docs