import re

from langchain_core.prompts import ChatPromptTemplate

from ingestion.config import LLM


# -----------------------------
# QUERY NORMALIZATION
# -----------------------------

def normalize_query(query):

    query = query.lower().strip()

    query = re.sub(r"\s+", " ", query)

    return query


# -----------------------------
# QUERY CLASSIFICATION
# -----------------------------

classification_prompt = ChatPromptTemplate.from_template("""
Classify query into ONE category.

Categories:
- FINANCIAL
- LEGAL
- TECHNICAL
- TABLE
- POLICY
- FAQ
- REPORT
- EMAIL

Query:
{query}

Return ONLY category name.
""")

classification_chain = classification_prompt | LLM


def classify_query(query):

    response = classification_chain.invoke({
        "query": query
    })

    intent = response.content.strip()

    print(f"\nQuery Intent: {intent}")

    return intent


# -----------------------------
# QUERY REWRITING
# -----------------------------

rewrite_prompt = ChatPromptTemplate.from_template("""
You are a search query optimizer.

Rewrite the query for better retrieval and web search.

STRICT RULES:
- Return ONLY the rewritten query
- Do NOT explain
- Do NOT add extra text
- Do NOT say "Here is rewritten query"
- Keep it concise
- Preserve original meaning

Original Query:
{query}
""")

rewrite_chain = rewrite_prompt | LLM


def rewrite_query(query):

    response = rewrite_chain.invoke({
        "query": query
    })

    rewritten_query = response.content.strip()

    print(f"\nRewritten Query: {rewritten_query}")

    return rewritten_query