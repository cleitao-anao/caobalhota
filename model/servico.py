from model.database import get_connection

class ServicoModel:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nome, valor_base, descricao FROM SERVICO ORDER BY nome ASC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar serviços: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_servico):
        conn = get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nome, valor_base, descricao FROM SERVICO WHERE id = %s", (id_servico,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar serviço: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def inserir(nome, valor_base, descricao):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO SERVICO (nome, valor_base, descricao) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nome, valor_base, descricao))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir serviço: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def atualizar(id_servico, nome, valor_base, descricao):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE SERVICO SET nome=%s, valor_base=%s, descricao=%s WHERE id=%s"
                cursor.execute(sql, (nome, valor_base, descricao, id_servico))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar serviço: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(id_servico):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM SERVICO WHERE id=%s", (id_servico,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar serviço: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
