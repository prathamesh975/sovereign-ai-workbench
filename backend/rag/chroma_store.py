import chromadb
from pathlib import Path


class ChromaStore:

    def __init__(self):

        storage_path = Path("knowledge_base/chroma")

        storage_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(storage_path)
        )

        self.collection = self.client.get_or_create_collection(
            name="organization_knowledge"
        )

    def add_documents(self, documents, ids, metadatas=None):

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query, n_results=3):

        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def count(self):

        return self.collection.count()