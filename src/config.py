# TODO: look into Pydantic for dataclass definitions

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


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
