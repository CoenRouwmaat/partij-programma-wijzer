# TODO: add attribute descriptions to docstring
# TODO: add keywords?
# TODO: add summary?

from dataclasses import dataclass
from uuid import UUID

from enums import Party, DocumentStructure
from langchain_core.documents import Document


@dataclass
class PartyDocumentChunk:
    """Represents a document chunk with content and other available information."""
    party: Party
    chapter: str
    section: str | None
    subsection: str | None
    content: str
    embedding: list[float] | None

    @classmethod
    def from_langchain_document(cls, doc: Document, party: Party) -> 'PartyDocumentChunk':
        """
        Creates a PartyDocumentChunk instance from a langchain Document object.

        It assumes the Document has the required keys in its metadata.
        """
        metadata = doc.metadata
        if DocumentStructure.CHAPTER not in metadata:
            raise ValueError(f"'{DocumentStructure.CHAPTER}' is not present in metadata.")

        return cls(
            party=party,
            chapter=metadata[DocumentStructure.CHAPTER],
            section=metadata.get(DocumentStructure.SECTION),
            subsection=metadata.get(DocumentStructure.SUBSECTION),
            content=doc.page_content,
            embedding=None
        )

    def to_postgres_tuple(self) -> tuple:
        """
        Returns the chunk's attributes as a tuple, correctly ordered for
        the PostgreSQL INSERT query's values clause.
        """
        postgres_tuple = (
            self.content,
            self.party,
            self.chapter,
            self.section,
            self.subsection,
            self.embedding
        )
        return postgres_tuple


@dataclass
class EnrichedPartyDocumentChunk:
    """Represents a document chunk with content, embedding and metadata."""
    id: UUID
    source: str
    source_id: UUID
    party: Party
    chapter: str
    chapter_id: UUID
    section: str | None
    section_id: UUID | None
    subsection: str | None
    subsection_id: UUID | None
    page_number: str | None  # TBD
    chunk_order: str | None  # TBD
    content: str
    embedding: list[float]
