def extract_metadata(block):

    content = block["content"]

    metadata = {

        "source": block.get("source"),

        "page": block.get("page"),

        "type": block.get("type"),

        "section": "general",

        "document_type": "UNKNOWN"
    }

    # -------------------------
    # SECTION DETECTION
    # -------------------------

    lowered = content.lower()

    if "revenue" in lowered:
        metadata["section"] = "Revenue"

    elif "policy" in lowered:
        metadata["section"] = "Policy"

    elif "risk" in lowered:
        metadata["section"] = "Risk"

    elif "summary" in lowered:
        metadata["section"] = "Summary"

    return metadata