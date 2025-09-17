# TODO: fix & clean image decoding & storing (doesn't render in markdown)
# TODO: add include_images flag
# TODO: create Party class / Literal / ?
# TODO: add args and return types to docstrings
# TODO: add module docstring
# TODO: move global vars to config file

import base64
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from mistralai import Mistral
from mistralai.models import OCRImageObject, OCRPageObject, OCRResponse

load_dotenv()

MISTRAL_OCR_MODEL = "mistral-ocr-latest"
MISTRAL_IMAGE_REF_FORMAT = "img-{i}.jpeg"

PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdfs"
JSON_DIR = DATA_DIR / "json"
MARKDOWN_DIR = DATA_DIR / "markdown_raw"
IMAGE_DIR = DATA_DIR / "images"


def upload_pdf_to_mistral(mistral_client: Mistral, party: str) -> str:
    """Upload a file from the pdf directory to Mistral, and returns the document url."""

    filename = f"Verkiezingsprogramma {party}.pdf"
    file = PDF_DIR / filename

    if not file.exists():
        raise ValueError(f"The file {file} does not exist.")

    logger.info(f"Uploading {filename} to Mistral...")
    uploaded_pdf = mistral_client.files.upload(
        file={
            "file_name": filename,
            "content": open(file, "rb"),
        },
        purpose="ocr"
    )
    signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

    return signed_url.url


def mistral_process_pdf(mistral_client: Mistral, document_url: str) -> OCRResponse:
    """Run Mistral OCR on an uploaded document and returns the response."""

    logger.info(f"Running OCR on document {document_url}...")
    ocr_response = mistral_client.ocr.process(
        model=MISTRAL_OCR_MODEL,
        document={
            "type": "document_url",
            "document_url": document_url,
        },
        include_image_base64=True
    )
    return ocr_response


def save_ocr_response_as_json(ocr_result: OCRResponse, party: str) -> None:
    """Save OCR response to the JSON folder."""
    response_json = ocr_result.model_dump_json()
    json_filename = JSON_DIR / f"{party}.json"

    logger.info(f"Writing {party} json document to {json_filename}...")
    with open(json_filename, 'w') as f:
        f.write(response_json)


def extract_image_data(image: OCRImageObject) -> bytes:
    """Get the base64 string, remove metadata, and decode to bytes."""

    base64_string = image.image_base64
    if not base64_string:
        raise ValueError("Unable to extract a base64 string from one of the images.")
    if ',' in base64_string:
        # The part before the comma is the metadata (e.g., 'data:image/jpeg;base64')
        # The part after is the actual base64 data we need
        base64_string = base64_string.split(',', 1)[1]

    image_data = base64.b64decode(base64_string)
    return image_data


def process_ocr_page_images(
        ocr_page: OCRPageObject,
        page_markdown: str,
        image_target_dir: Path
        ) -> str:
    """Process and save images from an OCR page object, and saves them to the party's image dir."""

    if ocr_page.images:
        logger.info(f"Processing images for page {ocr_page.index}...")
        image_target_dir.mkdir(exist_ok=True)
        img_id_pattern = r"^img-\d+\.jpeg$"

    for image in ocr_page.images:

        img_id = image.id
        if not re.match(img_id_pattern, img_id):
            raise ValueError(f"Image ID {img_id} does not have the pattern 'img_<number>.jpeg'.")
        new_image_url = img_id.replace('-', '_')  # eg "img_1.jpeg"

        new_image_path = image_target_dir / new_image_url

        image_data = extract_image_data(image=image)

        # Save the image to the new file path
        with open(new_image_path, 'wb') as f:
            f.write(image_data)

        page_markdown = page_markdown.replace(f"]({img_id})", f"]({new_image_path})")
    return page_markdown


def save_ocr_response_as_md(ocr_result: OCRResponse, party: str) -> None:
    """Save OCR response to the markdown folder."""

    md_filename = MARKDOWN_DIR / f"{party}.md"

    response_md = ""
    for page in ocr_result.pages:
        page_markdown = page.markdown

        image_page_markdown = process_ocr_page_images(
            ocr_page=page,
            page_markdown=page_markdown,
            image_target_dir=IMAGE_DIR / party
        )

        response_md += image_page_markdown + "\n\n"

    logger.info(f"Writing {party} markdown document to {md_filename}...")
    with open(md_filename, 'w') as f:
        f.write(response_md)


def process_pdf_to_markdown(party):
    """Process a single PDF file with OCR and store it as both a json and markdown file."""

    mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    doc_url = upload_pdf_to_mistral(mistral_client=mistral_client, party=party)
    ocr_result = mistral_process_pdf(mistral_client=mistral_client, document_url=doc_url)

    save_ocr_response_as_json(ocr_result=ocr_result, party=party)
    save_ocr_response_as_md(ocr_result=ocr_result, party=party)

    logger.info(f"{party} file succesfully processed and stored!")
