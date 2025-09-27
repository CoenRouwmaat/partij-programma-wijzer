# TODO: add generate_content_embedding, generate_query_embedding function to GeminiClient

from dataclasses import asdict
from pathlib import Path

from mistralai import Mistral
from mistralai.models import File, FileChunk, OCRResponse
import psycopg2
from psycopg2.extensions import connection, cursor

from src.config import (
    GeminiClientConfig,
    MistralClientConfig,
    PostgresClientConfig
)


class MistralClient:
    def __init__(self, config: MistralClientConfig):
        self._api_key = config.api_key
        if not self._api_key:
            raise ValueError("Could not find MISTRAL_API_KEY in the environment variables.")
        self.ocr_model = config.ocr_model
        self.mistral = Mistral(api_key=self._api_key)

    def upload_file_for_ocr(self, filename: str, filepath: Path) -> str:
        upload_result = self.mistral.files.upload(
            file=File(
                file_name=filename,
                content=open(filepath, "rb")
            ),
            purpose="ocr"
        )
        document_id = upload_result.id
        return document_id

    def run_ocr(self, document_id: str) -> OCRResponse:
        ocr_result = self.mistral.ocr.process(
            model=self.ocr_model,
            document=FileChunk(file_id=document_id),
            include_image_base64=False
        )
        return ocr_result


class GeminiClient:
    def __init__(self, config: GeminiClientConfig):
        self._api_key = config.api_key
        if not self._api_key:
            raise ValueError("Could not find MISTRAL_API_KEY in the environment variables.")
        self.embedding_model = config.embedding_model
        self.mistral = Mistral(api_key=self._api_key)


class PostgresClient:
    def __init__(self, config: PostgresClientConfig):
        self.connection: connection = psycopg2.connect(**asdict(config))
        self.cursor: cursor = self.connection.cursor()

    def create_pg_vector_extension(self):
        self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def insert(self, table_name: str, data_list: list[tuple]):

        # Roll back any previous failed transaction
        self.connection.rollback()

        insert_query_sql = """
            INSERT INTO {table} \
                (chunk_text, party_name, document_chapter, document_section, document_subsection, embedding)
            VALUES (%s, %s, %s, %s, %s, %s);
            """.format(table=table_name)
        self.cursor.executemany(query=insert_query_sql, vars_list=data_list)

        # Commit the changes
        self.connection.commit()

    def fetch_top_k(self, table_name: str, query_vector: list[float], top_k: int):
        # TODO: top_k value validation
        fetch_top_k_query_sql = """
            SELECT chunk_text, party_name, document_chapter, document_section, document_subsection
            FROM political_documents
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
            """
        self.cursor.execute(query=fetch_top_k_query_sql, vars=(query_vector, top_k))
