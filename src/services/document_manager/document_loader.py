from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class FileHandler:

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def load_pdf(self, file_path: str, source: str = None) -> list[Document]:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text.strip():
            return []

        doc = Document(
            page_content=text,
            metadata={"source": source or file_path}
        )
        return self.splitter.split_documents([doc])

    def load_text(self, text: str, metadata: dict = None) -> list[Document]:
        if not text.strip():
            return []

        doc = Document(
            page_content=text,
            metadata=metadata or {}
        )
        return self.splitter.split_documents([doc])
