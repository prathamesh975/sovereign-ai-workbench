from backend.validation.validator import Validator
from backend.harness.planner import Planner
from backend.harness.context_manager import ContextManager
from backend.harness.execution_loop import ExecutionLoop

from backend.document_processor import DocumentProcessor
from backend.rag.rag_pipeline import RAGPipeline


class Agent:

    def __init__(self):

        self.planner = Planner()
        self.context = ContextManager()
        self.execution_loop = ExecutionLoop()

        self.document_processor = DocumentProcessor()
        self.rag_pipeline = RAGPipeline()
        self.validator = Validator()

    def run(
        self,
        task: str,
        file_path: str
    ):

        # --------------------------------
        # Reset context for every new run
        # --------------------------------

        self.context = ContextManager()

        # --------------------------------
        # 1. Create plan
        # --------------------------------

        plan = self.planner.create_plan(task)

        self.context.set(
            "task",
            task
        )

        self.context.set(
            "plan",
            plan
        )

        self.context.set(
            "file_path",
            file_path
        )

        # --------------------------------
        # 2. Execute plan
        # --------------------------------

        def handle_step(step: str):

            # ==================================
            # STEP 1
            # ==================================

            if step == "Read the input document":

                result = self.document_processor.process(
                    file_path
                )

                self.context.set(
                    "document",
                    result
                )

                return (
                    f"Document processed using "
                    f"{result['method']}. "
                    f"Pages: {result['page_count']}"
                )

            # ==================================
            # STEP 2
            # ==================================

            if step == "Extract relevant information":

                document = self.context.get(
                    "document"
                )

                if not document:
                    return "Document not available."

                text = document.get(
                    "text",
                    ""
                )

                self.context.set(
                    "document_text",
                    text
                )

                return (
                    f"Extracted {len(text)} characters "
                    f"from the document."
                )

            # ==================================
            # STEP 3
            # ==================================

            if step == "Search the local knowledge base":

                results = self.rag_pipeline.retriever.search(
                    task,
                    n_results=3
                )

                self.context.set(
                    "rag_results",
                    results
                )

                return (
                    f"Retrieved {len(results)} "
                    f"relevant knowledge sources."
                )

            # ==================================
            # STEP 4
            # ==================================

            if step == "Analyze the findings":

                document_text = self.context.get(
                    "document_text",
                    ""
                )

                rag_results = self.context.get(
                    "rag_results",
                    []
                )

                if not document_text:
                    return (
                        "Analysis failed: "
                        "document content unavailable."
                    )

                if not rag_results:
                    return (
                        "Analysis completed without "
                        "additional knowledge sources."
                    )

                self.context.set(
                    "analysis",
                    {
                        "document_available": True,
                        "knowledge_sources": len(rag_results),
                        "document_characters": len(document_text)
                    }
                )

                self.context.set(
                    "analysis_sources",
                    rag_results
                )

                return (
                    "Inspection findings prepared using "
                    "the document and retrieved "
                    "organizational knowledge."
                )

            # ==================================
            # STEP 5
            # ==================================

            if step == "Generate the requested deliverable":

                document_text = self.context.get(
                    "document_text",
                    ""
                )

                rag_results = self.context.get(
                    "rag_results",
                    []
                )

                if not document_text:
                    return (
                        "Generation failed: "
                        "document content unavailable."
                    )

                context = self.rag_pipeline.build_context(
                    rag_results
                )

                generation_task = f"""
{task}

Use the inspection document and organizational
knowledge provided below.

DOCUMENT CONTENT:
----------------
{document_text}

ORGANIZATIONAL KNOWLEDGE:
-------------------------
{context}

STRICT REQUIREMENTS:

1. Use only the provided information.

2. Do not invent facts, measurements, names,
dates or approvals.

3. Clearly distinguish confirmed inspection
findings from recommendations.

4. Preserve all technical measurements exactly
as recorded.

5. Do not claim that any action has been approved
unless the source explicitly states that it has
been approved.

6. If information is missing, explicitly state
that it is missing.

7. Identify the source documents used.

8. Do not reuse information from previous
documents or previous agent runs.

Generate the requested deliverable professionally.
"""

                print(
                    f"[Agent] Generating output for: "
                    f"{file_path}"
                )

                response = self.rag_pipeline.llm.generate(
                    generation_task
                )

                self.context.set(
                    "generated_output",
                    response
                )

                self.context.set(
                    "generation_sources",
                    rag_results
                )

                return (
                    "Requested deliverable generated "
                    "by local Qwen."
                )

            # ==================================
            # STEP 6
            # ==================================

            if step == "Validate the output":

                output = self.context.get(
                    "generated_output",
                    ""
                )

                if not output:
                    return (
                        "Validation failed: "
                        "no output generated."
                    )

                validation_result = self.validator.validate(
                    output=output,
                    document_text=self.context.get(
                        "document_text",
                        ""
                    )
                )

                self.context.set(
                    "validation",
                    validation_result
                )

                if validation_result["passed"]:

                    return (
                        "Output validation passed."
                    )

                return (
                    "Output validation failed. "
                    f"Issues: {validation_result}"
                )

            # ==================================
            # UNKNOWN STEP
            # ==================================

            return f"Unknown step: {step}"

        # --------------------------------
        # Execute the complete plan
        # --------------------------------

        results = self.execution_loop.execute(
            plan,
            handle_step
        )

        self.context.set(
            "execution_results",
            results
        )

        # --------------------------------
        # Return final result
        # --------------------------------

        return {
            "task": task,

            "plan": plan,

            "execution": results,

            "output": self.context.get(
                "generated_output"
            ),

            "validation": self.context.get(
                "validation"
            ),

            # RAG / Knowledge Base sources
            "rag_sources": self.context.get(
                "rag_results",
                []
            ),

            "analysis_sources": self.context.get(
                "analysis_sources",
                []
            ),

            "generation_sources": self.context.get(
                "generation_sources",
                []
            )
        }