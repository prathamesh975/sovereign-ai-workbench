from backend.tools.ocr_tool import OCRTool


def main():

    print("\n==============================")
    print(" OCR TOOL TEST")
    print("==============================")

    image_path = "inputs/scanned_inspection.png"

    print(f"\nReading image: {image_path}")

    tool = OCRTool()

    text = tool.extract_text(image_path)

    print("\nExtracted OCR text:")
    print("--------------------------------")

    print(text)

    print("--------------------------------")
    print("OCR extraction successful.")


if __name__ == "__main__":
    main()