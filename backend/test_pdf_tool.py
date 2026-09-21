from backend.tools.pdf_tool import PDFTool


def main():

    tool = PDFTool()

    pdf_path = "inputs/inspection_report.pdf"

    print("\n==============================")
    print(" PDF EXTRACTION TEST")
    print("==============================")

    print(f"\nReading: {pdf_path}")

    result = tool.read(pdf_path)

    print("\nFile:")
    print(result["file"])

    print("\nPage count:")
    print(result["page_count"])

    print("\nHas text:")
    print(result["has_text"])

    print("\nExtracted text:")
    print("--------------------------------")

    print(result["text"])

    print("--------------------------------")
    print("PDF extraction successful.")


if __name__ == "__main__":
    main()