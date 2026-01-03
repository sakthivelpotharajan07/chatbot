import os
import glob
from app.tools.document_tool import load_document_text
from app.utils.simple_doc_qa import answer_from_document
from app.tools.web_search_tool import web_search

UPLOAD_DIR = "uploads"

def handle_document_query(user_question: str, document_path: str = None) -> str:
    
    if not document_path:
        # Check if uploads directory exists
        if not os.path.exists(UPLOAD_DIR):
             return "📂 No documents found. Please upload a document first."

        # Find the latest file in the uploads directory (only PDF or TXT)
        list_of_files = glob.glob(os.path.join(UPLOAD_DIR, "*"))
        supported_files = [f for f in list_of_files if f.lower().endswith(('.pdf', '.txt'))]
        
        if not supported_files:
            return "📂 No supported documents (PDF/TXT) found. Please upload a document first."
        
        document_path = max(supported_files, key=os.path.getctime)
    
    document_text = load_document_text(document_path)

    doc_answer = answer_from_document(
        document_text=document_text,
        question=user_question
    )

    if doc_answer:
        return f"📄 Answered from document '{os.path.basename(document_path)}':\n\n" + doc_answer

    return (
        "🌐 Not found in document. Answer from web:\n\n"
        + web_search(user_question)
    )
