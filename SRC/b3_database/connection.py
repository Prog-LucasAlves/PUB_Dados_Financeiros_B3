import os
from contextlib import contextmanager

import dotenv
from psycopg2 import pool

# Carrega as variáveis de ambiente
dotenv.load_dotenv(dotenv.find_dotenv())


class DatabaseConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            # Inicializa o pool com mínimo de 1 e máximo de 20 conexões
            cls._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB"),
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=int(os.getenv("POSTGRES_PORT", 5432)),
            )
        return cls._pool

    @classmethod
    @contextmanager
    def get_connection(cls):
        connection_pool = cls.get_pool()
        connection = connection_pool.getconn()
        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection_pool.putconn(connection)

    @classmethod
    def close_all(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None
