# Qdrant RAG System

A Retrieval-Augmented Generation (RAG) system built with FastAPI, Qdrant, LangChain, and OpenAI. Upload documents, store them as vector embeddings, and query them with natural language using an LLM.

## Architecture

```
Client -> FastAPI -> VectorStoreManager -> Qdrant (vector DB)
                  -> QuestionAnswerService -> OpenAI (LLM)
```

- **Document ingestion**: PDF upload with automatic chunking (RecursiveCharacterTextSplitter)
- **Embeddings**: OpenAI `text-embedding-3-large` (3072 dimensions)
- **Vector store**: Qdrant with cosine similarity
- **LLM**: OpenAI ChatGPT via LangChain LCEL chains
- **Sessions**: Per-session chat history support

## Setup

### Prerequisites

- Python 3.10+
- Qdrant instance (local or Docker)
- OpenAI API key

### Local Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
uvicorn server:app --reload
```

### Docker Setup

```bash
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
docker-compose up
```

This starts both the FastAPI app (port 8000) and Qdrant (port 6333).

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | (required) |
| `QDRANT_HOST` | Qdrant host | `localhost` |
| `QDRANT_PORT` | Qdrant port | `6333` |
| `LLM_TEMPERATURE` | LLM temperature | `0.7` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-3-large` |
| `API_KEY` | API key for authentication | (optional) |

## API Endpoints

### Collections

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vector_db/create_collection?collection_name=X` | Create a collection |
| DELETE | `/vector_db/delete_collection?collection_name=X` | Delete a collection |
| GET | `/vector_db/list_all_collections` | List all collections |
| GET | `/vector_db/get_collection_info?collection_name=X` | Get all docs in a collection |

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vector_db/add_doc_to_existing_collection` | Upload a PDF to a collection |
| POST | `/vector_db/add_text_to_existing_collection` | Add structured text to a collection |
| POST | `/vector_db/query_collection` | Semantic search on a collection |
| DELETE | `/vector_db/delete_doc_from_collection_by_name` | Delete a document by name |

### Chat (RAG)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/chat_agent` | Ask a question with RAG |
| GET | `/chat/history/{session_id}` | Get chat history for a session |
| DELETE | `/chat/history/{session_id}` | Clear a session's history |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (Qdrant connectivity) |

## Examples

```bash
# Create a collection
curl -X POST "http://localhost:8000/vector_db/create_collection?collection_name=my_docs"

# Upload a PDF
curl -X POST "http://localhost:8000/vector_db/add_doc_to_existing_collection?collection_name=my_docs" \
  -F "file=@document.pdf"

# Query with RAG
curl -X POST "http://localhost:8000/chat/chat_agent" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?", "collection_name": "my_docs", "k": 3, "session_id": "user-123"}'

# Health check
curl http://localhost:8000/health
```

## References

- [Qdrant](https://github.com/qdrant/qdrant-client)
- [LangChain](https://python.langchain.com/docs/integrations/vectorstores/qdrant/)
- [OpenAI](https://platform.openai.com/docs)

## License

MIT
