import pymysql
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model.database import get_connection

def update_enum():
    conn = get_connection()
    if not conn:
        print("Erro ao conectar ao banco.")
        return

    try:
        with conn.cursor() as cursor:
            # Change the status ENUM to include 'pago'
            print("Alterando tabela AGENDAMENTO...")
            cursor.execute("ALTER TABLE AGENDAMENTO MODIFY COLUMN status ENUM('agendado', 'iniciado', 'concluído', 'cancelado', 'pago');")
            
        conn.commit()
        print("Tabela alterada com sucesso!")
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_enum()
