from backend.rag.chroma_store import ChromaStore


def main():

    print("\n==============================")
    print(" CHROMADB TEST")
    print("==============================")

    store = ChromaStore()

    print("\nCollection:")
    print("organization_knowledge")

    print("\nCurrent document count:")
    print(store.count())

    print("\nChromaDB initialized successfully.")


if __name__ == "__main__":
    main()