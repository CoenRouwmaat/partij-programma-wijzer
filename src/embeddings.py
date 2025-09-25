# TODO: create gemini client config class
# TODO: convert embedding_content type to ndarray / tensor?

from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import EmbedContentConfig

from src.data_classes import PartyDocumentChunk

load_dotenv()


def format_embedding_content(chunk: PartyDocumentChunk) -> str:
    """Append chapter, section, subsection and content for embedding"""
    embedding_content = f"{chunk.chapter}\n{chunk.section}\n{chunk.subsection}\n{chunk.content}"
    return embedding_content


def generate_content_embeddings(gemini_client: Client, embedding_content: list[str]):
    embedding_result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=embedding_content
        )
    return embedding_result


def generate_query_embedding(gemini_client: Client, query: str) -> list[float]:
    query_embedding = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=EmbedContentConfig(
            task_type="retrieval_query",
            )
    )
    if not query_embedding.embeddings:
        raise ValueError(f"Gemini failed to return any embeddings for the query '{query}'.")
    embedding = query_embedding.embeddings[0]
    if not embedding.values:
        raise ValueError(f"Embedding for query '{query}' does not contain any values.")
    return embedding.values
