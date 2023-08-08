import os

import dotenv
import psycopg2

dotenv.load_dotenv(dotenv.find_dotenv())

# Conexão com o banco de dados (SELECT / INSERT / DELETE)


def conexao():
    """
    Função que tem o objetivo de de fazer a conexão com o banco de dados
    """
    con = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host="localhost",
    )

    return con


def in_dados(query):
    """
    Função que tem o objetivo de realizar - INSERT / DELETE no banco de dados
    """
    vcon = conexao()
    c = vcon.cursor()
    c.execute(query)
    vcon.commit()
    vcon.close()


def se_dados(query):
    """
    Função que tem o objetivo de realizar - SELECT no banco de dados
    """
    vcon = conexao()
    c = vcon.cursor()
    c.execute(query)
    rows = c.fetchall()
    vcon.commit()
    vcon.close()
    return rows


def bk(query, file):
    """
    Função que tem o objetivo de realizar um backup do banco de dados
    """
    vcon = conexao()
    c = vcon.cursor()
    c.copy_expert(query, file)


def verifica_conexao():
    """
    Função que tem o objetivo de verificar se
    conexão com o banco de dados foi realizada com sucesso
    """
    try:
        con = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host="localhost",
        )
        return con, True

    except psycopg2.Error:
        return False

#####
