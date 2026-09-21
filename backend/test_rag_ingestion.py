from backend.rag.document_ingester import DocumentIngester


def main():

    print("\n==============================")
    print(" RAG INGESTION TEST")
    print("==============================")

    ingester = DocumentIngester()

    directory = "knowledge_base/documents"

    print(f"\nKnowledge base: {directory}")

    count = ingester.ingest_directory(
        directory
    )

    print("\n------------------------------")
    print(f"Total chunks added: {count}")
    print("------------------------------")

    print("\nRAG ingestion successful.")


if __name__ == "__main__":
    main()