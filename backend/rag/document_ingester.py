from pathlib import Path

from backend.rag.chroma_store import ChromaStore


class DocumentIngester:

    def __init__(self):
        self.store = ChromaStore()

    def chunk_text(self, text, chunk_size=800, overlap=100):
        """
        Split text into overlapping chunks.
        """

        text = text.strip()

        if not text:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    def ingest_file(self, file_path):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Knowledge document not found: {file_path}"
            )

        text = path.read_text(
            encoding="utf-8"
        )

        chunks = self.chunk_text(text)

        if not chunks:
            return 0

        ids = []

        metadatas = []

        for index in range(len(chunks)):

            ids.append(
                f"{path.stem}_{index}"
            )

            metadatas.append(
                {
                    "source": path.name,
                    "path": str(path)
                }
            )

        self.store.add_documents(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

        return len(chunks)

    def ingest_directory(self, directory):

        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        total_chunks = 0

        for file_path in directory.glob("*.txt"):

            print(
                f"Ingesting: {file_path.name}"
            )

            count = self.ingest_file(
                str(file_path)
            )

            print(
                f"  → {count} chunks"
            )

            total_chunks += count

        return total_chunks