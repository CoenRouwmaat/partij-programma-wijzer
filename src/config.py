# TODO: look into Pydantic for dataclass definitions

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class FilePaths:
    project_root = Path.cwd()
    data_dir = project_root / "data"
    pdf_dir = data_dir / "pdfs"
    markdown_dir = data_dir / "markdown_raw"
    image_dir = data_dir / "images"
    clean_markdown_dir = data_dir / "markdown_clean"
    json_dir = data_dir / "json"
    chunk_dir = data_dir / "chunks"


@dataclass
class MarkdownHeaderTextSplitterConfig:
    headers_to_split_on = [
        ("#", "Hoofdstuk"),
        ("##", "Sectie"),
        ("###", "Subsectie"),
    ]
    strip_headers = True


@dataclass
class RecursiveCharacterTextSplitterConfig:
    max_chunk_size = 512
    chunk_overlap = 50
    separators = ["\n\n", ".\n", "\n", ".", " ", ""]
    keep_separator: Literal["start", "end"] = "end"
