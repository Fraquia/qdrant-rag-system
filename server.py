from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends

from src.config import settings
from src.logging_config import setup_logging
from src.auth import verify_api_key

setup_logging()
from src.endpoints.add_doc_to_existing_collection import router as add_doc_router
from src.endpoints.create_collection import router as create_collection_router
from src.endpoints.delete_collection import router as delete_collection_router
from src.endpoints.delete_doc_from_collection import router as delete_doc_from_collection_router
from src.endpoints.get_collection_info import router as get_collection_info_router
from src.endpoints.query_collection import router as query_collection_router
from src.endpoints.test_add_text_to_existing_collection import router as add_text_to_existing_collection_router
from src.endpoints.list_collections import router as list_collections_router
from src.endpoints.chat_agent import router as chat_agent_router
from src.endpoints.health import router as health_router


def create_app(debug=False, **kwargs):
    app = FastAPI(debug=debug, dependencies=[Depends(verify_api_key)], **kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(path="/")
    def main_page():
        return "Qdrant vector search API"

    app.include_router(add_doc_router)
    app.include_router(create_collection_router)
    app.include_router(delete_collection_router)
    app.include_router(delete_doc_from_collection_router)
    app.include_router(get_collection_info_router)
    app.include_router(query_collection_router)
    app.include_router(add_text_to_existing_collection_router)
    app.include_router(list_collections_router)
    app.include_router(chat_agent_router)
    app.include_router(health_router)
    return app


app = create_app()


