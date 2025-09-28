from src.clients import PostgresClient
from src.config import PostgresClientConfig
from src.data_classes import PartyDocumentChunk


def index_chunks_to_postgres_db(chunks: list[PartyDocumentChunk]):
    pg_client_config = PostgresClientConfig()
    pg_client = PostgresClient(config=pg_client_config)
    pg_client.create_pg_vector_extension()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS political_documents (
        id SERIAL PRIMARY KEY,
        chunk_text TEXT,
        party_name TEXT,
        document_chapter TEXT,
        document_section TEXT,
        document_subsection TEXT,
        embedding VECTOR(3072)
    );
    """

    pg_client.execute_query(query=create_table_query)

    pg_client.insert_chunks(
        table_name='political_documents',
        chunks=chunks
    )
