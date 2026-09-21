from paddleocr import PaddleOCR


class OCRTool:
    """
    Local OCR tool using PaddleOCR.
    """

    name = "ocr"

    def __init__(self):

        self.ocr = PaddleOCR(
            lang="en",
            enable_mkldnn=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def extract_text(self, image_path: str):

        result = self.ocr.predict(image_path)

        extracted_text = []

        for page_result in result:

            data = page_result.json

            if callable(data):
                data = data()

            if not data:
                continue

            ocr_data = data.get("res", data)

            texts = ocr_data.get(
                "rec_texts",
                []
            )

            for text in texts:

                if text and text.strip():
                    extracted_text.append(
                        text.strip()
                    )

        return "\n".join(extracted_text)