from pathlib import Path

from backend.tools.pdf_tool import PDFTool
from backend.tools.ocr_tool import OCRTool


class DocumentProcessor:

    def __init__(self):
        self.pdf_tool = PDFTool()
        self.ocr_tool = OCRTool()

    def process(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        # PDF processing
        if extension == ".pdf":

            result = self.pdf_tool.read(str(path))

            # Digital PDF
            if result.get("has_text") and result.get("text", "").strip():

                return {
                    "file": str(path),
                    "type": "pdf",
                    "method": "pymupdf",
                    "text": result["text"],
                    "page_count": result["page_count"]
                }

            # Scanned PDF
            return {
                "file": str(path),
                "type": "pdf",
                "method": "ocr_required",
                "text": "",
                "page_count": result["page_count"]
            }

        # Image processing
        if extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"]:

            text = self.ocr_tool.extract_text(str(path))

            return {
                "file": str(path),
                "type": "image",
                "method": "paddleocr",
                "text": text,
                "page_count": 1
            }

        raise ValueError(
            f"Unsupported file type: {extension}"
        )