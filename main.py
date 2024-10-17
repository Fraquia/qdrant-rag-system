import json
from langchain_core.documents import Document
from src.services.vector_store_services.vector_store_manager import VectorStoreManager

# vector store
vector_store = VectorStoreManager(port=6333, host="localhost")

# load data to test the vector store
docs = json.load(open('doc_test.json'))


### Support methods

def create_document(data):
    documents = list()
    if isinstance(data, dict):
        for key, value in data.items():
            doc = Document(page_content=value['descrizione'], metadata={"source": value['nome']})
            documents.append(doc)

    return documents


### Functions to interact with the vector store


def create_new_collection_and_data(collection_name: str, data):
    try:
        res = vector_store.create_collection(collection_name=collection_name)
        if res:
            doc_list = create_document(data)
            added_status = vector_store.add_documents_to_existing_collection(collection_name, doc_list)
        return {"message": f"Collection '{collection_name}' created successfully, and added documents: {added_status}"}
    except Exception as e:
        return {"error": str(e)}


def query(collection_name: str, query: str, k: int) -> list | dict:
    try:
        result = vector_store.retrieve_documents_from_collection(collection_name, query, k)
        return result
    except Exception as e:
        return {"error": str(e)}


# Testing the operations

#result = create_new_collection_and_data("test_collection", docs)
all_collections = vector_store.list_collections()

all_docs = vector_store.get_all_points("test_collection")
query_result = query(collection_name="test_collection", query="comodino", k=3)

delete_result = vector_store.delete_points_by_metadata_filter("test_collection", metadata={
    "source": "Frigorifero Combinato Bosch KGN39VI35"})
print('Done')
