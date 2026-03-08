from fastapi import APIRouter, HTTPException
from src.services.llm_service.retrieve_and_answer import QuestionAnswerService
from src.definitions.query_request import QueryRequest
import logging

router = APIRouter()

qa_service = QuestionAnswerService()


@router.post("/chat/chat_agent")
async def chat_agent(request: QueryRequest):
    try:
        result = qa_service.get_response(
            query=request.query,
            collection_name=request.collection_name,
            k=request.k,
            session_id=request.session_id,
        )
        return result
    except Exception as e:
        logging.error(f"Chat agent error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")


@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    history = qa_service.get_session_history(session_id)
    return {"session_id": session_id, "history": history}


@router.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    qa_service.clear_session(session_id)
    return {"message": f"Session '{session_id}' cleared"}
