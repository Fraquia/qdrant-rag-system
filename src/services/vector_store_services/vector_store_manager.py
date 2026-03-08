from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from typing import List, Any
import logging

from src.config import settings


class VectorStoreManager:

    def __init__(self) -> None:
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.embeddings = OpenAIEmbeddings(model=settings.embedding_model)

    def load_collection(self, collection_name: str) -> QdrantVectorStore | None:
        try:
            return QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embeddings,
            )
        except Exception as e:
            logging.error(f"Error loading collection: {e}")
            return None

    def _qdrant_filter_from_dict(self, filter: dict) -> Filter | None:
        if not filter:
            return None

        return Filter(
            must=[
                condition
                for key, value in filter.items()
                for condition in self._build_condition(key, value)
            ]
        )

    def _build_condition(self, key: str, value: Any) -> List[FieldCondition]:
        out = []

        if isinstance(value, dict):
            for _key, value in value.items():
                out.extend(self._build_condition(f"{key}.{_key}", value))
        elif isinstance(value, list):
            for _value in value:
                if isinstance(_value, dict):
                    out.extend(self._build_condition(f"{key}[]", _value))
                else:
                    out.extend(self._build_condition(f"{key}", _value))
        else:
            out.append(
                FieldCondition(
                    key=f"metadata.{key}",
                    match=MatchValue(value=value),
                )
            )

        return out

    def create_collection(self, collection_name: str) -> bool:
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
            )
            logging.info(f"Collection '{collection_name}' created successfully")
            return True
        except Exception as e:
            logging.error(f"Error creating collection: {e}")
            return False

    def add_documents_to_existing_collection(self, collection_name: str, documents: list[Document]) -> bool | dict:
        try:
            collection = self.load_collection(collection_name)
            uuids = [str(uuid4()) for _ in range(len(documents))]
            collection.add_documents(documents=documents, ids=uuids)
            return True
        except Exception as e:
            logging.error(f"Error adding documents: {e}")
            return {"error": str(e)}

    def retrieve_documents_from_collection(self, collection_name: str, query: str, k: int) -> list[str] | None:
        try:
            collection = self.load_collection(collection_name)
            results = collection.similarity_search(query=query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            logging.error(f"Error retrieving documents: {e}")
            return None

    def delete_document_from_collection(self, collection_name: str, document_id: str) -> bool:
        try:
            self.client.delete(
                collection_name=collection_name,
                points_selector={"must": [{"key": "title", "match": {"value": document_id}}]})
            return True
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            return False

    def delete_docs_by_metadata_filter(self, collection_name: str, metadata=None):
        try:
            res = self.client.delete(
                collection_name=collection_name,
                points_selector=self._qdrant_filter_from_dict(metadata),
            )
            return res
        except Exception as e:
            logging.error(f"Error deleting documents by filter: {e}")
            return None

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(collection_name=collection_name)
            logging.info(f"Collection '{collection_name}' deleted successfully")
            return True
        except Exception as e:
            logging.error(f"Error deleting collection: {e}")
            return False

    def list_collections(self):
        return self.client.get_collections()

    def get_all_docs_from_collection(self, collection_name: str):
        all_points, _ = self.client.scroll(
            collection_name=collection_name,
            with_vectors=True,
            limit=10000,
        )
        return all_points
