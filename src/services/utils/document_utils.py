from langchain_core.documents import Document


def create_document(data):
    documents = list()
    if isinstance(data, dict):
        for key, value in data.items():
            doc = Document(page_content=value['descrizione'], metadata={"source": value['nome']})
            documents.append(doc)

    elif isinstance(data, list):
        pass

    return documents

