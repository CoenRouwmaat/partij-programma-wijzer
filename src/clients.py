from dataclasses import asdict

import psycopg2
from psycopg2.extensions import connection, cursor

from src.config import PostgresClientConfig


class PostgresClient():

    def __init__(self, config: PostgresClientConfig):
        self.connection: connection = psycopg2.connect(**asdict(config))
        self.cursor: cursor = self.connection.cursor()
