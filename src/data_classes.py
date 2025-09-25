# TODO: add attribute descriptions to docstring
# TODO: add keywords?
# TODO: add summary?

from dataclasses import dataclass
from uuid import UUID

from enums import Party


@dataclass
class DocumentChunkData:
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
