from ingestion.config import LLM

from generation.prompt import (
    HALLUCINATION_PROMPT,
    ANSWER_GRADING_PROMPT
)


# -----------------------------------
# HALLUCINATION CHECK
# -----------------------------------

hallucination_chain = (
    HALLUCINATION_PROMPT | LLM
)


def check_hallucination(
    question,
    answer,
    documents
):

    context = "\n\n".join([
        doc.page_content
        for doc in documents
    ])

    response = hallucination_chain.invoke({
        "question": question,
        "answer": answer,
        "context": context[:12000]
    })

    print("\nHallucination Check:\n")

    print(response.content)

    return response.content


# -----------------------------------
# ANSWER GRADING
# -----------------------------------

answer_grading_chain = (
    ANSWER_GRADING_PROMPT | LLM
)


def grade_answer(
    question,
    answer
):

    response = answer_grading_chain.invoke({
        "question": question,
        "answer": answer
    })

    print("\nAnswer Grading:\n")

    print(response.content)

    return response.content