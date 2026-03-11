from model.database import get_connection

class ClienteModel:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cliente ORDER BY nome ASC")
                # format expected: (id, nome, cpf, telefone, email, endereco, admin)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_cliente):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cliente WHERE id = %s", (id_cliente,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def inserir(nome, cpf, telefone, email, endereco):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO cliente (nome, cpf, telefone, email, endereco) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (nome, cpf, telefone, email, endereco))
            conn.commit()
            return cursor.lastrowid # Return ID
        except Exception as e:
            print(f"Error inserting cliente: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def atualizar(id_cliente, nome, cpf, telefone, email, endereco):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE cliente SET nome=%s, cpf=%s, telefone=%s, email=%s, endereco=%s WHERE id=%s"
                cursor.execute(sql, (nome, cpf, telefone, email, endereco, id_cliente))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating cliente: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(id_cliente):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                # Delete pets associated with this client first, because of FK
                cursor.execute("DELETE FROM pet WHERE id_cliente = %s", (id_cliente,))
                # Now delete the client
                cursor.execute("DELETE FROM cliente WHERE id = %s", (id_cliente,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting cliente: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
