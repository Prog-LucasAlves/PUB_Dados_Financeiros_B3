from b3_database.connection import DatabaseConnectionManager

# Conexão com o banco de dados otimizada via Connection Pool (SELECT / INSERT / DELETE)


def conexao():
    """
    Função legada que obtém uma conexão do pool.
    Recomenda-se utilizar o context manager DatabaseConnectionManager.get_connection().
    """
    return DatabaseConnectionManager.get_pool().getconn()


def in_dados(query):
    """
    Função que realiza - INSERT / DELETE no banco de dados usando conexão segura do pool
    """
    with DatabaseConnectionManager.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)


def se_dados(query):
    """
    Função que realiza - SELECT no banco de dados usando conexão segura do pool
    """
    with DatabaseConnectionManager.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def bk(query, file):
    """
    Função que realiza um backup do banco de dados usando conexão segura do pool
    """
    with DatabaseConnectionManager.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.copy_expert(query, file)


def verifica_conexao():
    """
    Função que verifica se a conexão com o banco de dados está operacional
    """
    try:
        with DatabaseConnectionManager.get_connection() as conn:
            return conn, True
    except Exception:
        return False


#####
