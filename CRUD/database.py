"""
Módulo de conexão com o banco de dados LuxeVoyage (MySQL / Aiven Cloud).

As credenciais NÃO ficam mais no código — vêm de variáveis de ambiente
(arquivo .env, que fica fora do git). Veja .env.example.

Requer: pip install mysql-connector-python python-dotenv
"""
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do arquivo .env na raiz do projeto


def get_connection():
    """
    Abre e retorna uma nova conexão com o banco de dados.
    Lê host/porta/usuário/senha/banco das variáveis de ambiente.
    """
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )

    # Necessário pelo Aiven: o timezone da sessão não é global,
    # então é preciso setar a cada conexão nova (igual ao script de inserts).
    cursor = connection.cursor()
    cursor.execute("SET time_zone = 'America/Sao_Paulo'")
    cursor.close()

    return connection
