from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore

from src.config import load_settings

def build_vectorstore(docs: list[Document]) -> InMemoryVectorStore:
    settings = load_settings()
    embeddings = OpenAIEmbeddings(
        api_key = settings.openai_api_key,
        model = settings.openai_embedding_model,
    )

    return InMemoryVectorStore.from_documents(
        documents = docs,
        embedding = embeddings,
    )