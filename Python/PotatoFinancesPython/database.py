import mysql.connector
import pandas as pd

def conectar():
    """Estabelece a conexão com o banco de dados MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="S3nh@mySQL", 
        database="potato_finances"
    )

def inserir_transacao(tipo, descricao, valor, data, categoria, forma_pagamento):
    """C (Create): Insere uma nova receita, despesa ou investimento."""
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = """INSERT INTO transacoes (tipo, descricao, valor, data_transacao, categoria, forma_pagamento) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (tipo, descricao, valor, data, categoria, forma_pagamento)
        cursor.execute(sql, valores)
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERRO] Falha ao inserir transação: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

def ler_transacoes():
    """R (Read): Lê todas as transações e retorna organizadas em um DataFrame do Pandas."""
    conexao = None
    try:
        conexao = conectar()
        df = pd.read_sql("SELECT * FROM transacoes", conexao)
        return df
    except Exception as err:
        print(f"[ERRO] Falha ao ler transações: {err}")
        return pd.DataFrame()
    finally:
        if conexao: conexao.close()

def atualizar_transacao(id_transacao, tipo, descricao, valor, data, categoria, forma_pagamento):
    """U (Update): Altera os dados de uma transação existente pelo ID."""
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = """UPDATE transacoes 
                 SET tipo=%s, descricao=%s, valor=%s, data_transacao=%s, categoria=%s, forma_pagamento=%s 
                 WHERE id=%s"""
        valores = (tipo, descricao, valor, data, categoria, forma_pagamento, id_transacao)
        cursor.execute(sql, valores)
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERRO] Falha ao atualizar transação {id_transacao}: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

def deletar_transacao(id_transacao):
    """D (Delete): Exclui permanentemente uma transação do banco pelo ID."""
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM transacoes WHERE id = %s"
        cursor.execute(sql, (id_transacao,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERRO] Falha ao deletar transação {id_transacao}: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()