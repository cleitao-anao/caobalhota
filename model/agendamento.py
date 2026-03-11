from .database import get_connection

class AgendamentoModel:

    @staticmethod
    def listar_concluidos_nao_pagos(id_cliente):
        """Busca agendamentos com status 'concluído' para listar no Carrinho (ainda não foram pagos)"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT A.id, S.nome, S.valor_base, P.nome as pet_nome, A.data, A.hora
                    FROM AGENDAMENTO A
                    JOIN SERVICO S ON A.id_servico = S.id
                    JOIN PET P ON A.id_pet = P.id
                    WHERE A.id_cliente = %s AND A.status = 'concluído'
                """
                cursor.execute(sql, (id_cliente,))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def marcar_como_pago(id_agendamento):
        """Muda o status do agendamento para 'pago' para que não figure mais na aba de faturamento aberto"""
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE AGENDAMENTO SET status = 'pago' WHERE id = %s"
                cursor.execute(sql, (id_agendamento,))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao marcar agendamento como pago:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
