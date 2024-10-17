from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from typing import Any
import os


# todo: import template from a .txt file

# Set up the LLM (OpenAI)
llm = OpenAI(temperature=float(os.getenv("LLM_TEMPERATURE")))

# Example prompt template for answering based on context
prompt_template = """
You are a helpful assistant. Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:"""

# Define the prompt
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template
)


class QuestionAnswerChain():

    def __init__(self):
        self.chain = None
        self.chat_history = []
        self.N = 0
        self.count = 0
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.temperature = float(os.getenv("LLM_TEMPERATURE"))
        self.vector_store = VectorStoreManager()

    def __call__(self, query, collection_name: str, k: int) -> Any:
        if self.count == 0:
            print('Building the chain')
            self.build_chain(query, collection_name, k)
            self.count += 1

        return self.chain

    def build_chain(self, query, collection_name: str, k: int):
        # Here we assume the `query` contains the documents or information
        # to process (instead of a file)

        # Use Qdrant as vector store
        vector_store_collection = self.vector_store.load_collection(
            collection_name=collection_name)

        # Build the ConversationalRetrievalChain
        self.chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(
                temperature=self.temperature,
                openai_api_key=self.OPENAI_API_KEY),
            retriever=vector_store_collection.as_retriever(search_kwargs={"k": k}, filter=None),
            return_source_documents=True,
        )


def get_response(history, query, collection_name, k, app):
    chain = app(query, collection_name, k)  # Pass the collection name and k here

    # Get the response from the chain using the query and chat history
    result = chain({"question": query, 'chat_history': app.chat_history}, return_only_outputs=True)

    # Update the chat history with the latest question and answer
    app.chat_history += [(query, result["answer"])]

    return result['answer']

