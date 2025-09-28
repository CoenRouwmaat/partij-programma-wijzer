# TODO: refactor to separate client modules

from dataclasses import asdict
from pathlib import Path
import pandas as pd
from typing import Iterable

from loguru import logger
from mistralai import Mistral
from mistralai.models import File, FileChunk, OCRResponse
from google.genai import Client as Gemini
from google.genai.types import EmbedContentResponse
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
        self.include_images = config.include_images
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
            include_image_base64=self.include_images
        )
        return ocr_result


class GeminiClient:
    def __init__(self, config: GeminiClientConfig):
        self._api_key = config.api_key
        if not self._api_key:
            raise ValueError("Could not find GEMINI_API_KEY in the environment variables.")
        self.embedding_model = config.embedding_model
        self.query_embedding_config = config.query_embedding_config
        self.content_embedding_config = config.content_embedding_config
        self.gemini = Gemini(api_key=self._api_key)

    def embed_content(self, contents: Iterable[str]) -> list[list[float]]:
        embedding_result = self.gemini.models.embed_content(
            model=self.embedding_model,
            contents=contents,
            config=self.content_embedding_config
        )
        embedding_values = self._get_content_embedding_values(embedding_response=embedding_result)
        return embedding_values

    def embed_query(self, content: str) -> list[float]:
        embedding_result = self.gemini.models.embed_content(
            model=self.embedding_model,
            contents=content,
            config=self.query_embedding_config
        )
        embedding_values = self._get_query_embedding_values(embedding_response=embedding_result)
        return embedding_values

    @staticmethod
    def _get_content_embedding_values(embedding_response: EmbedContentResponse) -> list[list[float]]:
        """Checks if embedding and embedding values exist, and returns list of content value lists."""
        embeddings = embedding_response.embeddings
        if not embeddings:
            raise ValueError("Gemini content embedding result has no embeddings.")
        embedding_values = [embedding.values for embedding in embeddings]
        validated_embedding_values = [v for v in embedding_values if v is not None]
        if len(embedding_values) != len(embeddings):
            raise ValueError("Gemini content embedding exists with no values.")
        return validated_embedding_values

    @staticmethod
    def _get_query_embedding_values(embedding_response: EmbedContentResponse) -> list[float]:
        """Checks if embedding and embedding values exist, and returns list of query values."""
        embeddings = embedding_response.embeddings
        if not embeddings:
            raise ValueError("Gemini embedding result has no embeddings.")
        embedding_values = embeddings[0].values
        if not embedding_values:
            raise ValueError("Gemini query embedding has no values.")
        return embedding_values


class PostgresClient:
    def __init__(self, config: PostgresClientConfig):
        self.connection: connection = psycopg2.connect(**asdict(config))
        self.cursor: cursor = self.connection.cursor()

    def create_pg_vector_extension(self):
        sql_query = "CREATE EXTENSION IF NOT EXISTS vector;"
        self.execute_query(query=sql_query)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query: str) -> None:
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(f"An error has occured while executing the query '{query}'."
                         f"Error: {e}")
            self.connection.rollback()

    def list_tables(self) -> list[str]:
        sql_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        AND table_type = 'BASE TABLE';
        """
        self.execute_query(query=sql_query)
        tables_data = self.cursor.fetchall()
        table_names = [table[0] for table in tables_data]
        return table_names

    def get_table(self, table_name: str) -> pd.DataFrame:
        sql_query = f"SELECT * FROM {table_name}"
        try:
            df = pd.read_sql_query(sql=sql_query, con=self.connection)
            return df
        except Exception as e:
            logger.error(f"An error has occured while fetching the table '{table_name}': {e}")
            return pd.DataFrame()

    def clear_table(self, table_name: str):
        sql_query = f"TRUNCATE TABLE {table_name}"
        self.execute_query(query=sql_query)

    def insert(self, table_name: str, data_list: list[tuple]):

        insert_query_sql = """
            INSERT INTO {table} \
                (chunk_text, party_name, document_chapter, document_section, document_subsection, embedding)
            VALUES (%s, %s, %s, %s, %s, %s);
            """.format(table=table_name)
        try:
            self.cursor.executemany(query=insert_query_sql, vars_list=data_list)
            self.connection.commit()
        except Exception as e:
            logger.error(f"An error has occured while writing to '{table_name}': {e}")
            self.connection.rollback()

    def fetch_top_k(self, table_name: str, query_vector: list[float], top_k: int):
        # TODO: top_k value validation
        fetch_top_k_query_sql = """
            SELECT chunk_text, party_name, document_chapter, document_section, document_subsection
            FROM %s
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
            """
        self.cursor.execute(query=fetch_top_k_query_sql, vars=(table_name, query_vector, top_k))
