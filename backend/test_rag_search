from backend.rag.retriever import Retriever


def main():

    print("\n==============================")
    print(" RAG SEARCH TEST")
    print("==============================")

    retriever = Retriever()

    query = (
        "What should be done when a cooling "
        "water pump has mechanical seal leakage "
        "and coupling misalignment?"
    )

    print("\nQuery:")
    print(query)

    results = retriever.search(
        query,
        n_results=3
    )

    print("\nRelevant knowledge:")
    print("--------------------------------")

    for index, result in enumerate(
        results,
        start=1
    ):

        print(f"\n[{index}] Source:")
        print(result["source"])

        print("\nContent:")
        print(result["text"])

    print("\n--------------------------------")
    print("RAG search successful.")


if __name__ == "__main__":
    main()