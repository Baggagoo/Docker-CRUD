import os
import time
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL"""
    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        try:
            # Obtém a URL do banco de dados
            db_url = os.environ.get('DATABASE_URL')
            if not db_url:
                raise Exception("A variável de ambiente DATABASE_URL não está definida.")

            # Analisa a URL do banco de dados
            result = urlparse(db_url)
            conn = psycopg2.connect(
                host=result.hostname,
                database=result.path[1:],  # Remove a barra inicial
                user=result.username,
                password=result.password,
                port=result.port
            )
            return conn
        except psycopg2.OperationalError:
            attempts += 1
            print(f"Tentativa {attempts} de conexão com o banco de dados falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)

    raise Exception("Não foi possível conectar ao banco de dados após várias tentativas")

def close_db_connection(conn):
    """Fecha a conexão com o banco de dados"""
    if conn:
        conn.close()