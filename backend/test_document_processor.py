from backend.document_processor import DocumentProcessor


def main():

    print("\n==============================")
    print(" DOCUMENT PROCESSOR TEST")
    print("==============================")

    processor = DocumentProcessor()

    pdf_path = "inputs/inspection_report.pdf"

    print(f"\nProcessing: {pdf_path}")

    result = processor.process(pdf_path)

    print("\nFile:")
    print(result["file"])

    print("\nType:")
    print(result["type"])

    print("\nMethod:")
    print(result["method"])

    print("\nPage count:")
    print(result["page_count"])

    print("\nExtracted text:")
    print("--------------------------------")

    print(result["text"])

    print("--------------------------------")
    print("Document processing successful.")


if __name__ == "__main__":
    main()