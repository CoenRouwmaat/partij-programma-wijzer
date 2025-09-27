# TODO: convert embedding_content type to ndarray / tensor?

from dotenv import load_dotenv

from src.clients import GeminiClient
from src.data_classes import PartyDocumentChunk

load_dotenv()


def format_embedding_content(chunk: PartyDocumentChunk) -> str:
    """Append chapter, section, subsection and content for embedding"""
    embedding_content = f"{chunk.chapter}\n{chunk.section}\n{chunk.subsection}\n{chunk.content}"
    return embedding_content


def generate_content_embeddings(gemini_client: GeminiClient, embedding_content: list[str]) -> list[list[float]]:
    content_embedding: list[list[float]] = gemini_client.embed(
        contents=embedding_content,
        config=gemini_client.content_embedding_config
        )
    return content_embedding


def generate_query_embedding(gemini_client: GeminiClient, query: str) -> list[float]:
    query_embedding: list[float] = gemini_client.embed(
        contents=query,
        config=gemini_client.query_embedding_config
    )
    return query_embedding
