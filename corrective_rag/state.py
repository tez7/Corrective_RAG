from typing import TypedDict, List


class GraphState(TypedDict):

    question: str

    normalized_query: str

    query_intent: str

    rewritten_query: str

    retrieved_docs: list

    web_results: str

    retrieval_grade: dict

    hallucination_check: dict

    answer_grade: dict

    answer: str

    use_web_search: bool