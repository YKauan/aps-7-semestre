from .db_connector import get_db_connection
import mysql.connector

# Executa uma query select
def fetch_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return None, "Erro de conexão com o banco de dados."
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result, None
    except mysql.connector.Error as err:
        return None, str(err)
    finally:
        cursor.close()
        conn.close()

# executa consultas create, insert, delete
def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return None, "Erro de conexão com o banco de dados."
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid or cursor.rowcount, None
    except mysql.connector.Error as err:
        conn.rollback()
        return None, str(err)
    finally:
        cursor.close()
        conn.close()

# Retorna todos os indicadores
def get_all_indicadores():
    return fetch_query("SELECT * FROM indicadores")

# Retorna um inidicador especifico
def get_indicador_by_id(id):
    result, error = fetch_query("SELECT * FROM indicadores WHERE id = %s", (id,))
    if error:
        return None, error
    if not result:
        return None, None
    return result[0], None

# Adiciona um novo indicador
def add_new_indicador(data):
    query = """
        INSERT INTO indicadores (empresa, ano, consumo_agua_m3, residuos_ton, emissoes_co2_ton)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data['empresa'],
        data['ano'],
        data['consumo_agua_m3'],
        data['residuos_ton'],
        data['emissoes_co2_ton']
    )
    
    new_id, error = execute_query(query, params)
    if error:
        return None, error
    
    # Retorna o registro criado
    return get_indicador_by_id(new_id)

# Atualiza um indicador
def update_indicador_by_id(id, data):
    query = """
        UPDATE indicadores SET
        empresa = %s, ano = %s, consumo_agua_m3 = %s,
        residuos_ton = %s, emissoes_co2_ton = %s
        WHERE id = %s
    """
    params = (
        data.get('empresa'),
        data.get('ano'),
        data.get('consumo_agua_m3'),
        data.get('residuos_ton'),
        data.get('emissoes_co2_ton'),
        id
    )
    
    rowcount, error = execute_query(query, params)
    if error:
        return None, None, error # rowcount, record, error
    if rowcount == 0:
        return 0, None, None # Retorna 0 para nao encontrado
    
    # Retorna o registro atualizado
    updated_record, error = get_indicador_by_id(id)
    return rowcount, updated_record, error

# Deleta um indicador
def delete_indicador_by_id(id):
    rowcount, error = execute_query("DELETE FROM indicadores WHERE id = %s", (id,))
    if error:
        return 0, error
    return rowcount, None