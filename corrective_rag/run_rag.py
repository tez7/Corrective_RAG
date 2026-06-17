from corrective_rag.graph import (
    graph
)


if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk Question: "
        )

        if question.lower() == "exit":
            break

        result = graph.invoke({
            "question": question
        })

        print("\n" + "=" * 80)

        print("\nFINAL ANSWER")

        print("\n" + "=" * 80)

        print(result["answer"])