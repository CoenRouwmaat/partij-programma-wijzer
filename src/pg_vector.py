# TODO: add type hint for connection
# TODO: add PostgresClient object with PostgresConfig
# TODO: add error catching

import os

from dotenv import load_dotenv
import psycopg2
from psycopg2._psycopg import cursor

load_dotenv()


def connect_to_db(
    host: str | None = os.getenv("PG_HOST"),
    port: str | None = os.getenv("PG_PORT"),
    database: str | None = os.getenv("PG_DATABASE"),
    username: str | None = os.getenv("PG_USERNAME"),
    password: str | None = os.getenv("PG_PASSWORD")
) -> cursor:
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    # Enable the pgvector extension
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    return cursor
