# Corrective RAG System

## Overview

This project implements a production-style Corrective RAG (CRAG) system
using:

-   LangGraph
-   ChromaDB
-   HuggingFace Embeddings
-   Groq LLM
-   Hybrid Retrieval (Dense + BM25)
-   Reciprocal Rank Fusion (RRF)
-   Duplicate Chunk Removal
-   Retrieval Grading
-   Web Search Fallback (DuckDuckGo)
-   Hallucination Validation
-   LangSmith Observability

------------------------------------------------------------------------

## Project Structure

``` text
project/
│
├── data/
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
│
├── chroma_db/
│
├── ingestion/
│   ├── __init__.py
│   ├── run_ingestion.py
│   ├── loader.py
│   ├── parser.py
│   ├── metadata_extractor.py
│   ├── classifier.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vectordb.py
│   ├── pipeline.py
│   ├── schemas.py
│   └── config.py
│
├── retrieval/
│   ├── __init__.py
│   ├── query_processing.py
│   ├── retrieval_pipeline.py
│   ├── grading.py
│   └── utils.py
│
├── generation/
│   ├── __init__.py
│   ├── prompts.py
│   ├── generator.py
│   └── validation.py
│
├── corrective_rag/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   ├── graph.py
│   ├── web_search.py
│   └── run_rag.py
│
├── .env
├── requirements.txt
└── README.md

```

------------------------------------------------------------------------

## Ingestion Pipeline

1.  Load PDFs
2.  Parse text and tables
3.  Extract metadata
4.  Classify documents
5.  Chunk documents
6.  Create embeddings
7.  Store vectors in ChromaDB

Run:

``` bash
python -m ingestion.run_ingestion
```

------------------------------------------------------------------------

## Query Flow

1.  User asks a question
2.  Query normalization
3.  Query classification
4.  Dense retrieval
5.  BM25 retrieval
6.  Reciprocal Rank Fusion
7.  Duplicate chunk removal
8.  Chunk reordering
9.  Retrieval grading
10. Query rewrite and web search if required
11. Grounded answer generation
12. Hallucination validation
13. Final response

Run:

``` bash
python -m corrective_rag.run_rag
```

------------------------------------------------------------------------

## Fail-Fast Design

-   Hybrid retrieval improves robustness.
-   Duplicate chunks are removed using hash-based deduplication.
-   Retrieval quality is graded as:
    -   Relevant
    -   Ambiguous
    -   Irrelevant
-   Ambiguous or missing information triggers web search.
-   Generation is grounded strictly on retrieved context.
-   Hallucination checks validate answers before returning them.
-   LangSmith traces provide observability.

------------------------------------------------------------------------

## Environment Variables

``` env
GROQ_API_KEY=your_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=corrective-rag
```

------------------------------------------------------------------------

## Main Technologies

-   LangGraph
-   LangChain
-   ChromaDB
-   HuggingFace Embeddings
-   Groq
-   BM25
-   DuckDuckGo Search
-   LangSmith
