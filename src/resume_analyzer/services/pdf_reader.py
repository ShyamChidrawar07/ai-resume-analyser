
import pymupdf

class PdfReadError(ValueError):
    pass

class NoExtractableTextError(PdfReadError):
    def __init__(self, message: str = "No extractable text found in PDF file"):
        super().__init__(message)



class PdfTextExtractor:
    def extract_text(self, pdf_bytes: bytes) -> str:
        if not pdf_bytes:
            raise PdfReadError("PDF content is empty.")

        try:
            with pymupdf.open(stream=pdf_bytes,filetype="pdf") as document:
                pages = [page.get_text("text") for page in document]
                extracted_text = "\n".join(pages)

        except pymupdf.FileDataError as exc:
            raise PdfReadError("Invalid or unreadable PDF file.") from exc

        if not extracted_text.strip():
            raise NoExtractableTextError()

        return extracted_text
