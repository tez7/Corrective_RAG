from ingestion.config import LLM

from generation.prompt import (
    GENERATION_PROMPT
)


# -----------------------------------
# FORMAT CONTEXT
# -----------------------------------

def format_context(documents):

    context_parts = []

    for index, doc in enumerate(documents):

        metadata = doc.metadata

        chunk_text = f"""
Chunk {index + 1}

Source: {metadata.get("source")}
Page: {metadata.get("page")}
Type: {metadata.get("type")}
Section: {metadata.get("section")}

Content:
{doc.page_content}
"""

        context_parts.append(chunk_text)

    return "\n\n".join(context_parts)


# -----------------------------------
# GENERATE ANSWER
# -----------------------------------

generation_chain = GENERATION_PROMPT | LLM


def generate_answer(question, documents):

    print("\nGenerating Answer...")

    context = format_context(documents)

    response = generation_chain.invoke({
        "question": question,
        "context": context[:12000]
    })

    answer = response.content

    print("\nGenerated Answer:\n")

    print(answer)

    return answer