from backend.rag.rag_pipeline import RAGPipeline


def main():

    print("\n==============================")
    print(" RAG + LLM PIPELINE TEST")
    print("==============================")

    pipeline = RAGPipeline()

    task = """
Prepare an approval note for the inspection report.
Use the organization's maintenance SOP and approval
guidelines as supporting knowledge.
"""

    document_text = """
INDUSTRIAL EQUIPMENT INSPECTION REPORT

Report ID: IR-2026-001
Equipment: Cooling Water Pump P-101
Inspection Date: 28-Aug-2026
Department: Maintenance

INSPECTION FINDINGS

1. Minor leakage was observed near the mechanical seal.
2. Abnormal vibration of approximately 4.8 mm/s
   was recorded during operation.
3. Coupling alignment was found to require correction.
4. No visible cracks were observed on the pump casing.

RECOMMENDATION

1. Replacement of the mechanical seal.
2. Correction of coupling alignment.
3. Follow-up vibration measurement after maintenance.

The equipment should be monitored until corrective
maintenance is completed.
"""

    print("\nRunning RAG + LLM pipeline...")

    result = pipeline.generate(
        task=task,
        document_text=document_text
    )

    print("\nGenerated Output:")
    print("--------------------------------")
    print(result["response"])
    print("--------------------------------")

    print("\nSources Used:")

    for source in result["sources"]:
        print(
            f"- {source['source']}"
        )

    print("\nRAG + LLM pipeline successful.")


if __name__ == "__main__":
    main()