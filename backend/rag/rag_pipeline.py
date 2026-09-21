from backend.rag.retriever import Retriever
from backend.models.llm_generator import LLMGenerator


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.llm = LLMGenerator()

    def build_context(self, results):

        context_parts = []

        for result in results:

            context_parts.append(
                f"Source: {result['source']}\n"
                f"Content:\n{result['text']}"
            )

        return "\n\n".join(context_parts)

    def generate(
        self,
        task: str,
        document_text: str,
        n_results: int = 3
    ):

        # Retrieve relevant organizational knowledge
        results = self.retriever.search(
            task,
            n_results=n_results
        )

        context = self.build_context(results)

        prompt = f"""
You are a confidential industrial AI assistant.

Your task is to assist with the following request:

{task}

DOCUMENT CONTENT:
----------------
{document_text}

ORGANIZATIONAL KNOWLEDGE:
-------------------------
{context}

STRICT RULES:
1. Use only the information provided.
2. Do not invent facts, measurements, names, dates or approvals.
3. Clearly distinguish inspection findings from recommendations.
4. Preserve technical measurements exactly.
5. Do not claim that an action has been approved unless the
   source explicitly states that it has been approved.
6. If information is missing, state that it is missing.
7. Identify the source documents used.

Generate the requested output professionally.
"""

        print(
            f"[RAG] Prompt length: {len(prompt)} characters"
        )
        response = self.llm.generate(prompt)

        return {
            "response": response,
            "sources": results
        }