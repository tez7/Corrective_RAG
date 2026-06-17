from ddgs import DDGS


def web_search(query, max_results=5):

    print("\nWEB SEARCH TRIGGERED")

    print(f"\nSearching Web For: {query}")

    results_text = []

    with DDGS() as ddgs:

        results = ddgs.text(
            query,
            max_results=max_results
        )

        for result in results:

            body = result.get("body", "")

            title = result.get("title", "")

            results_text.append(
                f"Title: {title}\n"
                f"Content: {body}"
            )

    combined_results = "\n\n".join(results_text)

    print("\nWeb Results Retrieved")

    return combined_results