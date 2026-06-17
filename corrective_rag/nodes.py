import json

from retrieval.query_processing import (
    normalize_query,
    classify_query,
    rewrite_query
)

from retrieval.retrieval_pipeline import (
    hybrid_retrieval
)

from retrieval.grading import (
    grade_retrieval
)

from generation.generation import (
    generate_answer
)

from generation.validation import (
    check_hallucination,
    grade_answer
)

from corrective_rag.web_search import (
    web_search
)


# -----------------------------------
# SAFE JSON PARSER
# -----------------------------------

def safe_json_parse(text):

    try:

        cleaned = text.strip()

        cleaned = cleaned.replace(
            "```json",
            ""
        )

        cleaned = cleaned.replace(
            "```",
            ""
        )

        return json.loads(cleaned)

    except Exception as e:

        print("\nJSON Parsing Failed")

        print(e)

        return {}


# -----------------------------------
# QUERY PROCESSING NODE
# -----------------------------------

def process_query(state):

    print("\n" + "=" * 80)

    print("\nPROCESSING QUERY")

    print("\n" + "=" * 80)

    question = state["question"]

    # -----------------------------
    # NORMALIZE QUERY
    # -----------------------------

    normalized_query = normalize_query(
        question
    )

    print(
        f"\nNormalized Query:\n"
        f"{normalized_query}"
    )

    # -----------------------------
    # QUERY CLASSIFICATION
    # -----------------------------

    query_intent = classify_query(
        normalized_query
    )

    print(
        f"\nQuery Intent:\n"
        f"{query_intent}"
    )

    return {
        "normalized_query": normalized_query,
        "query_intent": query_intent
    }


# -----------------------------------
# RETRIEVE DOCUMENTS NODE
# -----------------------------------

def retrieve_documents(state):

    print("\n" + "=" * 80)

    print("\nRETRIEVING DOCUMENTS")

    print("\n" + "=" * 80)

    query = state["normalized_query"]

    docs = hybrid_retrieval(
        query=query,
        top_k=10
    )

    print(
        f"\nRetrieved Chunks Count: "
        f"{len(docs)}"
    )

    return {
        "retrieved_docs": docs
    }


# -----------------------------------
# RETRIEVAL EVALUATION NODE
# -----------------------------------

def evaluate_retrieval(state):

    print("\n" + "=" * 80)

    print("\nEVALUATING RETRIEVAL")

    print("\n" + "=" * 80)

    query = state["normalized_query"]

    docs = state["retrieved_docs"]

    # -----------------------------
    # GRADE RETRIEVAL
    # -----------------------------

    grade_raw = grade_retrieval(
        query,
        docs
    )

    grade = safe_json_parse(
        grade_raw
    )

    # -----------------------------
    # EXTRACT VALUES
    # -----------------------------

    category = grade.get(
        "category",
        "irrelevant"
    )

    missing_information = grade.get(
        "missing_information",
        True
    )

    reason = grade.get(
        "reason",
        "No reason provided"
    )

    # -----------------------------
    # WEB SEARCH DECISION
    # -----------------------------

    use_web_search = (
        category != "relevant"
        or missing_information
    )

    # -----------------------------
    # TERMINAL LOGGING
    # -----------------------------

    print(
        f"\nRetrieval Category: "
        f"{category}"
    )

    print(
        f"\nMissing Information: "
        f"{missing_information}"
    )

    print(
        f"\nReason:\n"
        f"{reason}"
    )

    print(
        f"\nUse Web Search: "
        f"{use_web_search}"
    )

    return {
        "retrieval_grade": grade,
        "use_web_search": use_web_search
    }


# -----------------------------------
# QUERY REWRITE NODE
# -----------------------------------

def rewrite_bad_query(state):

    print("\n" + "=" * 80)

    print("\nREWRITING QUERY")

    print("\n" + "=" * 80)

    original_query = state[
        "normalized_query"
    ]

    rewritten_query = rewrite_query(
        original_query
    )

    print(
        f"\nOriginal Query:\n"
        f"{original_query}"
    )

    print(
        f"\nRewritten Query:\n"
        f"{rewritten_query}"
    )

    return {
        "rewritten_query": rewritten_query
    }


# -----------------------------------
# WEB SEARCH NODE
# -----------------------------------

def search_web(state):

    print("\n" + "=" * 80)

    print("\nWEB SEARCH")

    print("\n" + "=" * 80)

    query = (
        state.get("rewritten_query")
        or state["normalized_query"]
    )

    results = web_search(query)

    return {
        "web_results": results
    }


# -----------------------------------
# ANSWER GENERATION NODE
# -----------------------------------

def generate(state):

    print("\n" + "=" * 80)

    print("\nGENERATING ANSWER")

    print("\n" + "=" * 80)

    docs = state["retrieved_docs"]

    web_results = state.get(
        "web_results",
        ""
    )

    # --------------------------------
    # ADD WEB RESULTS AS CONTEXT
    # --------------------------------

    if web_results:

        from langchain_core.documents import (
            Document
        )

        docs.append(
            Document(
                page_content=web_results,
                metadata={
                    "source": "web_search",
                    "type": "web"
                }
            )
        )

        print(
            "\nWeb search context added "
            "to generation"
        )

    # --------------------------------
    # GENERATE ANSWER
    # --------------------------------

    answer = generate_answer(
        state["question"],
        docs
    )

    return {
        "answer": answer
    }


# -----------------------------------
# ANSWER VALIDATION NODE
# -----------------------------------

def validate_answer(state):

    print("\n" + "=" * 80)

    print("\nVALIDATING ANSWER")

    print("\n" + "=" * 80)

    question = state["question"]

    answer = state["answer"]

    docs = state["retrieved_docs"]

    # --------------------------------
    # HALLUCINATION CHECK
    # --------------------------------

    hallucination_raw = (
        check_hallucination(
            question,
            answer,
            docs
        )
    )

    hallucination_result = (
        safe_json_parse(
            hallucination_raw
        )
    )

    # --------------------------------
    # ANSWER GRADING
    # --------------------------------

    answer_grade_raw = grade_answer(
        question,
        answer
    )

    answer_grade = safe_json_parse(
        answer_grade_raw
    )

    # --------------------------------
    # TERMINAL LOGGING
    # --------------------------------

    print(
        f"\nHallucination Check:\n"
        f"{hallucination_result}"
    )

    print(
        f"\nAnswer Grade:\n"
        f"{answer_grade}"
    )

    return {
        "hallucination_check":
            hallucination_result,

        "answer_grade":
            answer_grade
    }