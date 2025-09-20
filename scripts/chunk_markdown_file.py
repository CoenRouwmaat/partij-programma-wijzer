import argparse

from src.document_chunking import chunk_and_store_markdown_file
from src.utils import get_party_from_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a markdown file for a political party and store its chunks."
    )
    parser.add_argument(
        "party",
        type=get_party_from_string,
        help="The name of the political party to process (e.g., VVD, PVDA)."
    )
    args = parser.parse_args()
    chunk_and_store_markdown_file(args.party)
