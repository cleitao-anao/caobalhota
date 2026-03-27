from .database import get_connection

class DashboardModel:

    @staticmethod
    def resumo_estoque():
        """Total de produtos, soma de itens em estoque, produtos com estoque <= 5"""
        conn = get_connection()
        if not conn: return {'total_produtos': 0, 'total_itens': 0, 'estoque_baixo': 0, 'produtos_baixo': []}
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*), COALESCE(SUM(estoque), 0) FROM PRODUTO")
                row = cursor.fetchone()
                total_produtos = row[0]
                total_itens = int(row[1])

                cursor.execute("SELECT nome, estoque FROM PRODUTO WHERE estoque <= 5 ORDER BY estoque ASC")
                produtos_baixo = cursor.fetchall()

                return {
                    'total_produtos': total_produtos,
                    'total_itens': total_itens,
                    'estoque_baixo': len(produtos_baixo),
                    'produtos_baixo': produtos_baixo  # [(nome, estoque), ...]
                }
        except Exception as e:
            print("Erro resumo_estoque:", e)
            return {'total_produtos': 0, 'total_itens': 0, 'estoque_baixo': 0, 'produtos_baixo': []}
        finally:
            conn.close()

    @staticmethod
    def resumo_vendas():
        """Nº de vendas, faturamento total, ticket médio"""
        conn = get_connection()
        if not conn: return {'num_vendas': 0, 'faturamento': 0.0, 'ticket_medio': 0.0}
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*), COALESCE(SUM(valor_total), 0), COALESCE(AVG(valor_total), 0) FROM VENDA")
                row = cursor.fetchone()
                return {
                    'num_vendas': row[0],
                    'faturamento': float(row[1]),
                    'ticket_medio': float(row[2])
                }
        except Exception as e:
            print("Erro resumo_vendas:", e)
            return {'num_vendas': 0, 'faturamento': 0.0, 'ticket_medio': 0.0}
        finally:
            conn.close()

    @staticmethod
    def top_produtos_vendidos(limit=5):
        """Top N produtos mais vendidos por quantidade"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT P.nome, SUM(IV.quantidade) as total_qtd
                    FROM ITEM_VENDA IV
                    JOIN PRODUTO P ON IV.id_produto = P.id
                    WHERE IV.tipo_item = 'produto'
                    GROUP BY P.nome
                    ORDER BY total_qtd DESC
                    LIMIT %s
                """
                cursor.execute(sql, (limit,))
                return cursor.fetchall()  # [(nome, total_qtd), ...]
        except Exception as e:
            print("Erro top_produtos:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def top_servicos_vendidos(limit=5):
        """Top N serviços mais realizados por quantidade"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT S.nome, SUM(IV.quantidade) as total_qtd
                    FROM ITEM_VENDA IV
                    JOIN SERVICO S ON IV.id_servico = S.id
                    WHERE IV.tipo_item = 'servico'
                    GROUP BY S.nome
                    ORDER BY total_qtd DESC
                    LIMIT %s
                """
                cursor.execute(sql, (limit,))
                return cursor.fetchall()
        except Exception as e:
            print("Erro top_servicos:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def resumo_agendamentos():
        """Contagem de agendamentos por status"""
        conn = get_connection()
        if not conn: return {}
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT status, COUNT(*) FROM AGENDAMENTO GROUP BY status")
                rows = cursor.fetchall()
                return {row[0]: row[1] for row in rows}
        except Exception as e:
            print("Erro resumo_agendamentos:", e)
            return {}
        finally:
            conn.close()

    @staticmethod
    def resumo_clientes():
        """Total clientes e total pets"""
        conn = get_connection()
        if not conn: return {'total_clientes': 0, 'total_pets': 0}
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM CLIENTE")
                total_cli = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM PET")
                total_pet = cursor.fetchone()[0]
                return {'total_clientes': total_cli, 'total_pets': total_pet}
        except Exception as e:
            print("Erro resumo_clientes:", e)
            return {'total_clientes': 0, 'total_pets': 0}
        finally:
            conn.close()

    @staticmethod
    def vendas_ultimos_7dias():
        """Faturamento agrupado por dia nos últimos 7 dias"""
        conn = get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT data_venda, COALESCE(SUM(valor_total), 0) as total
                    FROM VENDA
                    WHERE data_venda >= CURDATE() - INTERVAL 7 DAY
                    GROUP BY data_venda
                    ORDER BY data_venda ASC
                """
                cursor.execute(sql)
                return cursor.fetchall()  # [(date, total), ...]
        except Exception as e:
            print("Erro vendas_7dias:", e)
            return []
        finally:
            conn.close()
