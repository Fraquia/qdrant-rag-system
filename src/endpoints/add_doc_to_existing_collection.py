from fastapi import APIRouter, UploadFile, File
from PyPDF2 import PdfReader

from src.services.vector_store_services.vector_store_manager import VectorStoreManager

router = APIRouter()

@router.post("/add_doc_to_existing_collection")
def add_doc_to_existing_collection(collection_name: str, file: UploadFile = File(...)):
    # document loader
    contents = file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    reader = PdfReader("temp.pdf")
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    return None

    # collection manager


