from model.database import get_connection

class PetModel:
    @staticmethod
    def listar_por_cliente(id_cliente):
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pet WHERE id_cliente = %s ORDER BY nome ASC", (id_cliente,))
                # Expected: (id, id_cliente, nome, especie, raca, idade, porte, cuidados_especiais)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def inserir(id_cliente, nome, especie, raca, idade, porte, cuidados_especiais):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO pet (id_cliente, nome, especie, raca, idade, porte, cuidados_especiais) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (id_cliente, nome, especie, raca, idade, porte, cuidados_especiais))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting pet: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def atualizar(id_pet, nome, especie, raca, idade, porte, cuidados_especiais):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE pet SET nome=%s, especie=%s, raca=%s, idade=%s, porte=%s, cuidados_especiais=%s WHERE id=%s"
                cursor.execute(sql, (nome, especie, raca, idade, porte, cuidados_especiais, id_pet))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating pet: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(id_pet):
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM pet WHERE id = %s", (id_pet,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting pet: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
