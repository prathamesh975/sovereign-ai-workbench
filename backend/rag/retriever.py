from backend.rag.chroma_store import ChromaStore


class Retriever:

    def __init__(self):
        self.store = ChromaStore()

    def search(self, query, n_results=3):

        result = self.store.search(
            query=query,
            n_results=n_results
        )

        documents = result.get(
            "documents",
            [[]]
        )[0]

        metadatas = result.get(
            "metadatas",
            [[]]
        )[0]

        results = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            results.append(
                {
                    "text": document,
                    "source": metadata.get(
                        "source",
                        "unknown"
                    )
                }
            )

        return results