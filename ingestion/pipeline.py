from ingestion.loader import (
    load_pdf_files
)

from ingestion.parser import (
    extract_pdf_blocks
)

from ingestion.metadata_extractor import (
    extract_metadata
)

from ingestion.classifier import (
    classify_document
)

from ingestion.chunker import (
    chunk_blocks
)

from ingestion.vectordb import (
    store_chunks
)


# -----------------------------------
# MAIN INGESTION PIPELINE
# -----------------------------------

def run_ingestion(data_folder):

    print("\n" + "=" * 80)

    print("\nSTARTING INGESTION PIPELINE")

    print("\n" + "=" * 80)

    # --------------------------------
    # LOAD PDF FILES
    # --------------------------------

    pdf_files = load_pdf_files(
        data_folder
    )

    print(
        f"\nPDF Files Found: "
        f"{len(pdf_files)}"
    )

    all_blocks = []

    # --------------------------------
    # PROCESS EACH PDF
    # --------------------------------

    for pdf in pdf_files:

        pdf_path = pdf["file_path"]

        file_name = pdf["file_name"]

        print("\n" + "-" * 80)

        print(
            f"\nProcessing PDF:\n"
            f"{file_name}"
        )

        # -----------------------------
        # PARSE PDF
        # -----------------------------

        blocks = extract_pdf_blocks(
            pdf_path=pdf_path,
            file_name=file_name
        )

        print(
            f"\nBlocks Extracted: "
            f"{len(blocks)}"
        )

        # -----------------------------
        # METADATA EXTRACTION
        # -----------------------------

        enriched_blocks = []

        for block in blocks:

            metadata = extract_metadata(
                block
            )

            # -------------------------
            # DOCUMENT CLASSIFICATION
            # -------------------------

            document_type = classify_document(
                block["content"]
            )

            block.update(metadata)

            block[
                "document_type"
            ] = document_type

            enriched_blocks.append(
                block
            )

        print(
            f"\nMetadata Extraction Completed"
        )

        print(
            f"\nDocument Classification Completed"
        )

        all_blocks.extend(
            enriched_blocks
        )

    # --------------------------------
    # CHUNKING
    # --------------------------------

    print("\n" + "=" * 80)

    print("\nSTARTING CHUNKING")

    print("\n" + "=" * 80)

    documents = chunk_blocks(
        all_blocks
    )

    # --------------------------------
    # VECTOR STORAGE
    # --------------------------------

    print("\n" + "=" * 80)

    print("\nSTORING IN VECTOR DATABASE")

    print("\n" + "=" * 80)

    store_chunks(
        documents
    )

    print("\n" + "=" * 80)

    print("\nINGESTION COMPLETED")

    print("\n" + "=" * 80)