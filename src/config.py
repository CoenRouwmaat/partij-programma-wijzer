from pathlib import Path


class FilePaths:
    PROJECT_ROOT = Path.cwd()
    DATA_DIR = PROJECT_ROOT / "data"
    PDF_DIR = DATA_DIR / "pdfs"
    MARKDOWN_DIR = DATA_DIR / "markdown_raw"
    IMAGE_DIR = DATA_DIR / "images"
    CLEAN_MARKDOWN_DIR = DATA_DIR / "markdown_clean"
    JSON_DIR = DATA_DIR / "json"
    CHUNK_DIR = DATA_DIR / "chunks"
