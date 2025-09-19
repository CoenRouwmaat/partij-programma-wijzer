from src.mistral_ocr import process_pdf_to_markdown

from src.enums import Party

if __name__ == "__main__":
    party = Party.VVD
    process_pdf_to_markdown(party)
