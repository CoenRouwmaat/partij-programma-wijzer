# TODO: add upload, process & parse_response functions to MistralClient

from dataclasses import asdict

from mistralai import Mistral
import psycopg2
from psycopg2.extensions import connection, cursor

from src.config import (
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


class PostgresClient:
    def __init__(self, config: PostgresClientConfig):
        self.connection: connection = psycopg2.connect(**asdict(config))
        self.cursor: cursor = self.connection.cursor()
