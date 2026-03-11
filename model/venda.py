from .database import get_connection
from datetime import date

class VendaModel:

    @staticmethod
    def finalizar_venda(id_cliente, itens_carrinho, valor_total):
        """
        Recebe itens do carrinho na estrutura:
        [
           {'tipo': 'produto', 'id': id_produto, 'qtd': 1, 'preco': preco},
           {'tipo': 'servico', 'id': id_servico, 'qtd': 1, 'preco': preco, 'id_agendamento': ag_id}
        ]
        """
        conn = get_connection()
        if not conn: return False

        hoje = date.today().isoformat()

        try:
            with conn.cursor() as cursor:
                # 1. Criar a VENDA
                sql_venda = "INSERT INTO VENDA (id_cliente, data_venda, valor_total) VALUES (%s, %s, %s)"
                cursor.execute(sql_venda, (id_cliente, hoje, valor_total))
                id_venda = cursor.lastrowid

                # 2. Inserir ITEMS e alterar estoque ou status do agendamento
                for item in itens_carrinho:
                    if item['tipo'] == 'produto':
                        sql_item = "INSERT INTO ITEM_VENDA (id_venda, id_produto, quantidade, valor_unitario, tipo_item) VALUES (%s, %s, %s, %s, 'produto')"
                        cursor.execute(sql_item, (id_venda, item['id'], item['qtd'], item['preco']))

                        sql_estoque = "UPDATE PRODUTO SET estoque = estoque - %s WHERE id = %s"
                        cursor.execute(sql_estoque, (item['qtd'], item['id']))

                    elif item['tipo'] == 'servico':
                        sql_item = "INSERT INTO ITEM_VENDA (id_venda, id_servico, quantidade, valor_unitario, tipo_item) VALUES (%s, %s, %s, %s, 'servico')"
                        cursor.execute(sql_item, (id_venda, item['id'], item['qtd'], item['preco']))

                        if 'id_agendamento' in item and item['id_agendamento']:
                            sql_ag_status = "UPDATE AGENDAMENTO SET status = 'pago' WHERE id = %s"
                            cursor.execute(sql_ag_status, (item['id_agendamento'],))

            conn.commit()
            return True
        except Exception as e:
            print("Erro ao finalizar venda:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
