import pymupdf
from pathlib import Path


class PDFTool:
    """
    Extracts text from machine-readable PDF files.
    """

    name = "pdf_reader"

    def read(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "PDFTool only accepts PDF files."
            )

        document = pymupdf.open(file_path)

        pages = []

        for page_number, page in enumerate(
            document,
            start=1
        ):

            text = page.get_text("text")

            pages.append({
                "page": page_number,
                "text": text.strip()
            })

        document.close()

        full_text = "\n\n".join(
            page["text"]
            for page in pages
            if page["text"]
        )

        return {
            "file": str(path),
            "page_count": len(pages),
            "pages": pages,
            "text": full_text,
            "has_text": bool(full_text.strip())
        }