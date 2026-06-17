from langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

table_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=100
)


# -----------------------------------
# CHUNK BLOCKS
# -----------------------------------

def chunk_blocks(blocks):

    documents = []

    for block in blocks:

        content = block["content"]

        metadata = {

            "source":
                block.get("source"),

            "page":
                block.get("page"),

            "type":
                block.get("type"),

            "section":
                block.get(
                    "section",
                    "general"
                ),

            "document_type":
                block.get(
                    "document_type",
                    "UNKNOWN"
                )
        }

        # --------------------------------
        # SPLIT INTO CHUNKS
        # --------------------------------

        chunks = text_splitter.split_text(
            content
        )

        # --------------------------------
        # CREATE DOCUMENT OBJECTS
        # --------------------------------

        for chunk_index, chunk in enumerate(chunks):

            chunk_metadata = metadata.copy()

            chunk_metadata[
                "chunk_id"
            ] = (
                f"{metadata.get('source')}"
                f"_p{metadata.get('page')}"
                f"_c{chunk_index}"
            )

            documents.append(

                Document(

                    page_content=chunk,

                    metadata=chunk_metadata
                )
            )

    print(
        f"\nTotal Chunks Created: "
        f"{len(documents)}"
    )

    return documents