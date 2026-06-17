from langchain_core.prompts import ChatPromptTemplate

from ingestion.config import LLM


grading_prompt = ChatPromptTemplate.from_template("""
You are a retrieval evaluator.

Question:
{question}

Retrieved Context:
{context}

Evaluate retrieved chunks carefully.

Categories:

1. relevant
- chunks clearly answer question

2. irrelevant
- chunks unrelated to question

3. ambiguous
- chunks partially related, conflicting,
  unclear, or noisy

Also detect:
- missing_information

Return STRICT JSON:

{{
  "category": "relevant",
  "missing_information": false,
  "reason": "..."
}}
""")


grading_chain = grading_prompt | LLM


def grade_retrieval(question, docs):

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    response = grading_chain.invoke({
        "question": question,
        "context": context[:10000]
    })

    print("\nRetrieval Grading:\n")

    print(response.content)

    return response.content