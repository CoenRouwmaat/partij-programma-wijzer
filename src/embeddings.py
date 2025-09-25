# TODO: create gemini client config class
# TODO: convert embedding_content type to ndarray / tensor?

from dotenv import load_dotenv
from google.genai import Client

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
