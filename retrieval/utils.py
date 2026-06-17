import hashlib


# -----------------------------
# HASH CHUNK
# -----------------------------

def generate_chunk_hash(text):

    normalized = text.lower().strip()

    normalized = normalized.replace("\n", " ")

    hash_value = hashlib.md5(
        normalized[:150].encode()
    ).hexdigest()

    return hash_value


# -----------------------------
# REMOVE DUPLICATE CHUNKS
# -----------------------------

def deduplicate_chunks(documents):

    unique_docs = []

    seen_hashes = set()

    for doc in documents:

        chunk_hash = generate_chunk_hash(
            doc.page_content
        )

        if chunk_hash not in seen_hashes:

            seen_hashes.add(chunk_hash)

            unique_docs.append(doc)

    return unique_docs


# -----------------------------
# PRINT RETRIEVED CHUNKS
# -----------------------------

def print_chunks(documents):

    print("\nRetrieved Chunks:\n")

    for index, doc in enumerate(documents):

        metadata = doc.metadata

        print("\n" + "-" * 80)

        print(f"\nChunk {index + 1}")

        print(
            f"\nDocument: "
            f"{metadata.get('source')}"
        )

        print(
            f"\nType: "
            f"{metadata.get('type')}"
        )

        print(
            f"\nPage: "
            f"{metadata.get('page')}"
        )

        print(
            f"\nSection: "
            f"{metadata.get('section')}"
        )

        print(
            f"\nDocument Type: "
            f"{metadata.get('document_type')}"
        )

        print("\nContent Preview:\n")

        print(doc.page_content[:250])