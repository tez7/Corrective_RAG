import pdfplumber
import re


def detect_section(text):

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        # simple heading heuristic
        if (
            len(line) < 80
            and line.isupper()
        ):
            return line

    return "general"


def extract_pdf_blocks(
    pdf_path,
    file_name
):

    blocks = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_num, page in enumerate(pdf.pages):

            # -------------------------
            # TEXT EXTRACTION
            # -------------------------

            text = page.extract_text()

            if text:

                blocks.append({

                    "content": text,

                    "type": "text",

                    "page": page_num + 1,

                    "source": file_name
                })

            # -------------------------
            # TABLE EXTRACTION
            # -------------------------

            tables = page.extract_tables()

            for table in tables:

                table_text = "\n".join([
                    " | ".join(
                        cell or ""
                        for cell in row
                    )
                    for row in table
                ])

                blocks.append({

                    "content":
                        f"TABLE:\n{table_text}",

                    "type": "table",

                    "page": page_num + 1,

                    "source": file_name
                })

    return blocks