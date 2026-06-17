from langchain_core.prompts import ChatPromptTemplate


# -----------------------------------
# STRICT GROUNDED GENERATION
# -----------------------------------

GENERATION_PROMPT = ChatPromptTemplate.from_template("""
You are a strict retrieval-augmented AI assistant.

You MUST answer ONLY from the provided context.

STRICT RULES:
- Do NOT use outside knowledge
- IF there is information present in table or information comes from table then use exact words from table only
- Do NOT hallucinate
- Do NOT assume anything
- If answer is not fully available in context, say:
  "I could not find sufficient information in the provided documents."
- If table data exists, use it carefully
- Mention comparisons clearly if present
- Keep answer factual and grounded

Question:
{question}

Context:
{context}
""")


# -----------------------------------
# HALLUCINATION CHECK PROMPT
# -----------------------------------

HALLUCINATION_PROMPT = ChatPromptTemplate.from_template("""
You are a hallucination detection system.

Question:
{question}

Generated Answer:
{answer}

Retrieved Context:
{context}

Check:
1. Is answer grounded in context?
2. Any hallucinated claims?
3. Any unsupported information?

Return STRICT JSON:

{{
  "grounded": true,
  "hallucination": false,
  "reason": "..."
}}
""")


# -----------------------------------
# ANSWER QUALITY PROMPT
# -----------------------------------

ANSWER_GRADING_PROMPT = ChatPromptTemplate.from_template("""
Evaluate answer quality.

Question:
{question}

Answer:
{answer}

Check:
1. Is question fully answered?
2. Is answer clear?
3. Is important information missing?

Return STRICT JSON:

{{
  "complete": true,
  "clear": true,
  "missing_information": false,
  "reason": "..."
}}
""")