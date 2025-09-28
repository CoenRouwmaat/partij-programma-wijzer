# TODO: clean up & add error handling
# TODO: write documentation & logging
# TODO: enrich chunks for optimal embedding

import json
from dataclasses import asdict
from pathlib import Path

from langchain_text_splitters import (MarkdownHeaderTextSplitter,
                                      RecursiveCharacterTextSplitter)
from loguru import logger

from src.config import (FilePaths, MarkdownHeaderTextSplitterConfig,
                        RecursiveCharacterTextSplitterConfig)
from src.data_classes import PartyDocumentChunk
from src.enums import Party


class CustomMarkdownSplitter:
    """
    A custom splitter that first splits a markdown document by headers
    and then performs a recursive character split on the resulting chunks.
    """
    def __init__(
        self,
        markdown_splitter_config: MarkdownHeaderTextSplitterConfig,
        recursive_splitter_config: RecursiveCharacterTextSplitterConfig
    ):
        """Initializes the two underlying text splitters with the given configurations."""
        self.markdown_splitter = MarkdownHeaderTextSplitter(**asdict(markdown_splitter_config))
        self.recursive_splitter = RecursiveCharacterTextSplitter(**asdict(recursive_splitter_config))

    def split(self, markdown_str: str) -> list[PartyDocumentChunk]:
        """
        Splits a markdown string into chunks using a two-step process.

        Args:
            markdown_str: The raw markdown content as a string.

        Returns:
            A list of Document objects, each representing a final chunk.
        """
        # Step 1: Split the markdown string by headers
        md_header_splits = self.markdown_splitter.split_text(markdown_str)

        # Step 2: Recursively split the header chunks into smaller chunks
        langchain_chunks = self.recursive_splitter.split_documents(md_header_splits)

        party_document_chunks = [
            PartyDocumentChunk.from_langchain_document(chunk) for chunk in langchain_chunks]

        return party_document_chunks


def chunk_markdown_file(markdown_str: str) -> list[PartyDocumentChunk]:
    markdown_splitter_config = MarkdownHeaderTextSplitterConfig()
    recursive_splitter_config = RecursiveCharacterTextSplitterConfig()

    splitter = CustomMarkdownSplitter(
        markdown_splitter_config=markdown_splitter_config,
        recursive_splitter_config=recursive_splitter_config
    )
    chunks = splitter.split(markdown_str)
    return chunks


def write_chunks_to_json(chunks: list[PartyDocumentChunk], chunk_path: Path) -> None:

    with open(chunk_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            # Convert the chunk object to a JSON string
            chunk_dict = chunk.to_json()
            json_line = json.dumps(chunk_dict)
            # Write the JSON string to a new line
            f.write(json_line)

    logger.info(f"Chunks saved to {chunk_path}")


def read_and_chunk_markdown_file(party: Party) -> list[PartyDocumentChunk]:
    clean_markdown_file = FilePaths.clean_markdown_dir / f"{party}_clean.md"

    with open(clean_markdown_file, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    chunks = chunk_markdown_file(markdown_string)
    return chunks


def chunk_and_store_markdown_file(party: Party) -> None:
    chunks = read_and_chunk_markdown_file(party=party)
    chunk_path = FilePaths.chunk_dir / f"{party}_chunks.jsonl"

    write_chunks_to_json(chunks, chunk_path)
