from dotenv import load_dotenv

from src.data_classes import PartyDocumentChunk

load_dotenv()


def format_embedding_content(chunk: PartyDocumentChunk) -> str:
    """Append chapter, section, subsection and content for embedding"""
    embedding_content = f"{chunk.chapter}\n{chunk.section}\n{chunk.subsection}\n{chunk.content}"
    return embedding_content
