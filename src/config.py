# TODO: look into Pydantic for dataclass definitions
# TODO: refactor to folder

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from google.genai import types


@dataclass
class FilePaths:
    project_root: Path = Path.cwd()
    data_dir: Path = project_root / "data"
    pdf_dir: Path = data_dir / "pdfs"
    markdown_dir: Path = data_dir / "markdown_raw"
    image_dir: Path = data_dir / "images"
    clean_markdown_dir: Path = data_dir / "markdown_clean"
    json_dir: Path = data_dir / "json"
    chunk_dir: Path = data_dir / "chunks"


@dataclass
class MistralConfig:
    mistral_ocr_model: str = "mistral-ocr-latest"


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
class GeminiEmbeddingConfig:
    model: str = "gemini-embedding-001"
    config = types.EmbedContentConfig(
        task_type="retrieval_document",
        output_dimensionality=3072
    )
