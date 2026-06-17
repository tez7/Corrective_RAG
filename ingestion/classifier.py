from langchain_core.prompts import ChatPromptTemplate
from ingestion.config import LLM


prompt = ChatPromptTemplate.from_template("""
Classify the document into ONE category.

Categories:
- Invoice
- Research
- Legal
- Medical
- Contract
- Resume
- Financial
- General

Document:
{content}

Return ONLY category name.
""")


chain = prompt | LLM


def classify_document(text):

    response = chain.invoke({
        "content": text[:4000]
    })

    return response.content.strip()