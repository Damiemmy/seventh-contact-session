import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_connection():
    """Create and return a PostgreSQL connection."""
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url, row_factory=dict_row)

    required = ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing database setting(s): "
            + ", ".join(missing)
            + ". Configure DATABASE_URL or copy .env.example to .env "
              "and fill in your PostgreSQL credentials."
        )

    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        row_factory=dict_row,
    )


def initialize_database():
    """Create the tasks table if it does not already exist."""
    query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            is_completed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
