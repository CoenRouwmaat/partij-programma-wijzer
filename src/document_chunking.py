# TODO: clean up & add error handling
# TODO: write documentation & logging
# TODO: check if this method is compatible for other parties
# TODO: add config classes for high level parameter configuration

import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import (MarkdownHeaderTextSplitter,
                                      RecursiveCharacterTextSplitter)
from loguru import logger

from config import FilePaths
from enums import Party


HEADERS_TO_SPLIT_ON = [
    ("#", "Hoofdstuk"),
    ("##", "Sectie"),
    ("###", "Subsectie"),
]

MAX_CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def chunk_markdown_file(markdown_str: str) -> list[Document]:

    markdown_splitter = MarkdownHeaderTextSplitter(HEADERS_TO_SPLIT_ON, strip_headers=True)
    md_header_splits = markdown_splitter.split_text(markdown_str)
    # print(len(md_header_splits))
    # print(md_header_splits[50])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", ".\n", "\n", ".", " ", ""],
        keep_separator='end'
    )

    chunks = text_splitter.split_documents(md_header_splits)
    # print(len(chunks))
    # for i in range(10, 30):
    #     print(chunks[i])

    return chunks


def write_chunks_to_json(chunks: list[Document], chunk_path: Path) -> None:

    with open(chunk_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            # Convert the chunk object to a JSON string
            chunk_dict = chunk.to_json()
            json_line = json.dumps(chunk_dict)
            # Write the JSON string to a new line
            f.write(json_line)

    logger.info(f"Chunks saved to {chunk_path}")


def chunk_and_store_markdown_file(party: Party) -> None:
    clean_markdown_file = FilePaths.CLEAN_MARKDOWN_DIR / f"{party}_clean.md"

    with open(clean_markdown_file, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    chunks = chunk_markdown_file(markdown_string)

    chunk_path = FilePaths.CHUNK_DIR / f"{party}_chunks.jsonl"

    write_chunks_to_json(chunks, chunk_path)
