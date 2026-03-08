import os
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.config import settings


PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "qa_prompt.txt"


def _load_prompt() -> ChatPromptTemplate:
    template = PROMPT_PATH.read_text()
    return ChatPromptTemplate.from_template(template)


class QuestionAnswerService:

    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.llm = ChatOpenAI(temperature=settings.llm_temperature)
        self.prompt = _load_prompt()
        self.sessions: dict[str, list[tuple[str, str]]] = {}

    def get_response(self, query: str, collection_name: str, k: int, session_id: str | None = None) -> dict:
        collection = self.vector_store.load_collection(collection_name)
        retriever = collection.as_retriever(search_kwargs={"k": k})

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        answer = chain.invoke(query)

        if session_id:
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            self.sessions[session_id].append((query, answer))

        return {
            "answer": answer,
            "session_id": session_id,
        }

    def get_session_history(self, session_id: str) -> list[tuple[str, str]]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        self.sessions.pop(session_id, None)
