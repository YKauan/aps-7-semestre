import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import errorcode

# Carrega as variaveis de ambiente do arquivo .env
load_dotenv()

# Pega as configuracoes do banco
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

# Cria a conexao com o banco
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Verifique seu usuario ou senha do MySQL.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Erro: O banco de dados '{db_config['database']}' nao existe.")
        else:
            print(err)
        return None