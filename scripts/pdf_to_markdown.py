import argparse

from src.mistral_ocr import process_pdf_to_markdown
from src.utils import get_party_from_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a PDF for a political party and convert to Markdown."
    )
    parser.add_argument(
        "party",
        type=get_party_from_string,
        help="The name of the political party to process (e.g., VVD, PVDA)."
    )
    args = parser.parse_args()
    process_pdf_to_markdown(args.party)
