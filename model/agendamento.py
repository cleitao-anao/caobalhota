from .database import get_connection

class AgendamentoModel:

    @staticmethod
    def listar_todos():
        """Lista todos os agendamentos com JOINs para nomes"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT A.id, C.nome as cliente, P.nome as pet, S.nome as servico,
                           F.nome as funcionario, A.data, A.hora, A.status,
                           A.cor_tintura, A.observacoes, S.valor_base,
                           A.id_cliente, A.id_pet, A.id_servico, A.id_funcionario
                    FROM AGENDAMENTO A
                    JOIN CLIENTE C ON A.id_cliente = C.id
                    JOIN PET P ON A.id_pet = P.id
                    JOIN SERVICO S ON A.id_servico = S.id
                    JOIN FUNCIONARIO F ON A.id_funcionario = F.id
                    ORDER BY A.data DESC, A.hora DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar agendamentos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def listar_por_status(status):
        """Lista agendamentos filtrados por status"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT A.id, C.nome as cliente, P.nome as pet, S.nome as servico,
                           F.nome as funcionario, A.data, A.hora, A.status,
                           A.cor_tintura, A.observacoes, S.valor_base
                    FROM AGENDAMENTO A
                    JOIN CLIENTE C ON A.id_cliente = C.id
                    JOIN PET P ON A.id_pet = P.id
                    JOIN SERVICO S ON A.id_servico = S.id
                    JOIN FUNCIONARIO F ON A.id_funcionario = F.id
                    WHERE A.status = %s
                    ORDER BY A.data ASC, A.hora ASC
                """
                cursor.execute(sql, (status,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar agendamentos por status: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def inserir(id_cliente, id_pet, id_servico, id_funcionario, data, hora, cor_tintura='', observacoes=''):
        """Insere um novo agendamento com status 'agendado'"""
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO AGENDAMENTO 
                    (id_cliente, id_pet, id_servico, id_funcionario, data, hora, status, cor_tintura, observacoes)
                    VALUES (%s, %s, %s, %s, %s, %s, 'agendado', %s, %s)
                """
                cursor.execute(sql, (id_cliente, id_pet, id_servico, id_funcionario, data, hora, cor_tintura, observacoes))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir agendamento: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def atualizar_status(id_agendamento, novo_status):
        """Atualiza o status de um agendamento"""
        conn = get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE AGENDAMENTO SET status = %s WHERE id = %s"
                cursor.execute(sql, (novo_status, id_agendamento))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def listar_concluidos_nao_pagos(id_cliente):
        """Busca agendamentos com status 'concluído' para listar no Carrinho"""
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
        """Muda o status do agendamento para 'pago'"""
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

    @staticmethod
    def listar_funcionarios():
        """Lista todos os funcionários para o dropdown do agendamento"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nome, cargo FROM FUNCIONARIO ORDER BY nome ASC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar funcionários: {e}")
            return []
        finally:
            conn.close()
