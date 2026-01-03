from pathlib import Path
from pypdf import PdfReader

def load_document_text(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.lower()

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8").lower()

    raise ValueError("Unsupported document type")
