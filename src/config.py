# TODO: look into Pydantic for dataclass definitions
# TODO: refactor to folder

from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from google.genai.types import EmbedContentConfig

from src.utils import find_project_root

load_dotenv()


@dataclass
class FilePaths:
    project_root: Path = find_project_root()
    data_dir: Path = project_root / "data"
    pdf_dir: Path = data_dir / "pdfs"
    markdown_dir: Path = data_dir / "markdown_raw"
    image_dir: Path = data_dir / "images"
    clean_markdown_dir: Path = data_dir / "markdown_clean"
    short_markdown_dir: Path = data_dir / "markdown_short"
    json_dir: Path = data_dir / "json"
    chunk_dir: Path = data_dir / "chunks"


@dataclass
class MistralClientConfig:
    api_key: str = os.getenv("MISTRAL_API_KEY", "")
    ocr_model: str = "mistral-ocr-latest"
    include_images: bool = False


@dataclass
class MarkdownHeaderTextSplitterConfig:
    headers_to_split_on: list[tuple[str, str]] = field(
        default_factory=lambda: [
            ("#", "Hoofdstuk"),
            ("##", "Sectie"),
            ("###", "Subsectie"),
        ]
    )
    strip_headers: bool = True


@dataclass
class RecursiveCharacterTextSplitterConfig:
    chunk_size: int = 512
    chunk_overlap: int = 50
    separators: list[str] = field(
        default_factory=lambda: ["\n\n", ".\n", "\n", ".", " ", ""]
    )
    keep_separator: Literal["start", "end"] = "end"


@dataclass
class GeminiClientConfig:
    api_key: str = field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY", "")
    )
    embedding_model: str = "gemini-embedding-001"
    output_dimensionality: int = 3072
    embedding_batch_size: int = 100
    query_embedding_config: EmbedContentConfig = field(init=False)
    content_embedding_config: EmbedContentConfig = field(init=False)

    def __post_init__(self) -> None:
        """Initializes fields that depend on other class attributes."""

        self.query_embedding_config = EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=self.output_dimensionality
        )
        self.content_embedding_config = EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=self.output_dimensionality
        )


@dataclass
class PostgresClientConfig:
    host: str | None = os.getenv("PG_HOST")
    port: str | None = os.getenv("PG_PORT")
    dbname: str | None = os.getenv("PG_DATABASE")
    user: str | None = os.getenv("PG_USERNAME")
    password: str | None = os.getenv("PG_PASSWORD")
