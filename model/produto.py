from model.database import get_connection

class ProdutoModel:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo, nome, descricao, preco, estoque FROM PRODUTO")
            return cursor.fetchall()
        except: return []
        finally: conn.close()
        
    @staticmethod
    def buscar_por_id(id_produto):
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo, nome, descricao, preco, estoque FROM PRODUTO WHERE id = %s", (id_produto,))
            return cursor.fetchone()
        except: return None
        finally: conn.close()

    @staticmethod
    def inserir(codigo, nome, descricao, preco, estoque):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO PRODUTO (codigo, nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (codigo, nome, descricao, preco, estoque))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally: conn.close()

    @staticmethod
    def atualizar(id_produto, codigo, nome, descricao, preco, estoque):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "UPDATE PRODUTO SET codigo=%s, nome=%s, descricao=%s, preco=%s, estoque=%s WHERE id=%s"
            cursor.execute(sql, (codigo, nome, descricao, preco, estoque, id_produto))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally: conn.close()

    @staticmethod
    def deletar(id_produto):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PRODUTO WHERE id=%s", (id_produto,))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally: conn.close()
