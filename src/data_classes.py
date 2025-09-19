# TODO: add attribute descriptions to docstring
# TODO: add keywords?
# TODO: add summary?

from dataclasses import dataclass
from typing import Optional
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
    section: Optional[str]
    section_id: Optional[UUID]
    subsection: Optional[str]
    subsection_id: Optional[UUID]
    page_number: Optional[str]  # TBD
    chunk_order: Optional[str]  # TBD
    content: str
    embedding: list[float]
