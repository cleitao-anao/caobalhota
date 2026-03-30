import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model.database import get_connection

def insert_test_data():
    conn = get_connection()
    if not conn:
        print("Erro ao conectar ao banco de dados.")
        return
    
    try:
        with conn.cursor() as cursor:
            # 1. Funcionários
            print("Inserindo Funcionários...")
            funcionarios_data = [
                ("Carlos Silva", "Dono", "11999999999", "carlos@petz.com", "carlos", "1234"),
                ("Ana Costa", "Atendente", "11988888888", "ana@petz.com", "ana", "1234"),
                ("Lucas Souza", "Esteticista", "11977777777", "lucas@petz.com", "lucas", "1234")
            ]
            funcionario_ids = []
            for f in funcionarios_data:
                cursor.execute("INSERT INTO funcionario (nome, cargo, telefone, email, login, senha) VALUES (%s, %s, %s, %s, %s, %s)", f)
                funcionario_ids.append(cursor.lastrowid)
            
            # 2. Clientes
            print("Inserindo Clientes...")
            clientes_data = [
                ("João Mendes", "111.111.111-11", "11955554444", "joao@email.com", "Rua das Flores, 123", None),
                ("Maria Clara", "222.222.222-22", "11933332222", "maria@email.com", "Av. Brasil, 456", None),
                ("Pedro Gomes", "333.333.333-33", "11911110000", "pedro@email.com", "Rua do Sol, 789", None)
            ]
            cliente_ids = []
            for c in clientes_data:
                cursor.execute("INSERT INTO cliente (nome, cpf, telefone, email, endereco, admin) VALUES (%s, %s, %s, %s, %s, %s)", c)
                cliente_ids.append(cursor.lastrowid)

            # 3. Pets
            print("Inserindo Pets...")
            pets_data = [
                (cliente_ids[0], "Rex", "Cão", "Golden Retriever", "3 anos", "grande", "Nenhum"),
                (cliente_ids[0], "Mimi", "Gato", "Siamês", "1 ano", "pequeno", "Não gosta de água"),
                (cliente_ids[1], "Max", "Cão", "Pug", "2 anos", "pequeno", "Problemas respiratórios"),
                (cliente_ids[2], "Piu", "Pássaro", "Calopsita", "6 meses", "pequeno", "Gaiola sempre limpa")
            ]
            pet_ids = []
            for p in pets_data:
                cursor.execute("INSERT INTO pet (id_cliente, nome, especie, raca, idade, porte, cuidados_especiais) VALUES (%s, %s, %s, %s, %s, %s, %s)", p)
                pet_ids.append(cursor.lastrowid)

            # 4. Produtos
            print("Inserindo Produtos...")
            produtos_data = [
                ("PRD-001", "Ração Golden", "Ração premium para cães adultos", 150.00, 20),
                ("PRD-002", "Shampoo Neutro", "Shampoo para cães e gatos", 25.50, 50),
                ("PRD-003", "Coleira Ajustável", "Coleira M", 35.00, 15),
                ("PRD-004", "Petisco Sabor Carne", "Petisco sem corantes", 12.00, 100),
                ("PRD-005", "Brinquedo Osso", "Osso de borracha", 18.00, 30)
            ]
            produto_ids = []
            for prod in produtos_data:
                cursor.execute("INSERT INTO produto (codigo, nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s, %s)", prod)
                produto_ids.append(cursor.lastrowid)

            # 5. Serviços
            print("Inserindo Serviços...")
            servicos_data = [
                ("Tosa Básica", 50.00, "Tosa higiênica e básica"),
                ("Banho Completo", 40.00, "Banho com shampoo neutro e condicionador"),
                ("Hidratação", 30.00, "Hidratação profunda da pelagem"),
                ("Corte de Unhas", 15.00, "Aparação segura das unhas"),
                ("Consulta Veterinária", 120.00, "Avaliação geral de saúde")
            ]
            servico_ids = []
            for serv in servicos_data:
                cursor.execute("INSERT INTO servico (nome, valor_base, descricao) VALUES (%s, %s, %s)", serv)
                servico_ids.append(cursor.lastrowid)

            # 6. Vendas & Item_Venda
            print("Inserindo Vendas e Itens de Venda...")
            vendas_data = [
                (cliente_ids[0], "2026-03-01", 175.50),  # Ração + Shampoo
                (cliente_ids[1], "2026-03-05", 35.00),   # Coleira
            ]
            for i, v in enumerate(vendas_data):
                cursor.execute("INSERT INTO venda (id_cliente, data_venda, valor_total) VALUES (%s, %s, %s)", v)
                venda_id = cursor.lastrowid
                
                if i == 0:
                    cursor.execute("INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario, tipo_item) VALUES (%s, %s, %s, %s, %s)", (venda_id, produto_ids[0], 1, 150.00, 'produto'))
                    cursor.execute("INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario, tipo_item) VALUES (%s, %s, %s, %s, %s)", (venda_id, produto_ids[1], 1, 25.50, 'produto'))
                else:
                    cursor.execute("INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario, tipo_item) VALUES (%s, %s, %s, %s, %s)", (venda_id, produto_ids[2], 1, 35.00, 'produto'))

            # 7. Agendamentos
            print("Inserindo Agendamentos...")
            agendamentos_data = [
                (cliente_ids[0], pet_ids[0], servico_ids[1], funcionario_ids[2], "2026-03-15", "10:00:00", "agendado", None, "Cão dócil"),
                (cliente_ids[1], pet_ids[2], servico_ids[0], funcionario_ids[2], "2026-03-16", "14:30:00", "agendado", None, "Cuidado com o focinho")
            ]
            for agen in agendamentos_data:
                cursor.execute("INSERT INTO agendamento (id_cliente, id_pet, id_servico, id_funcionario, data, hora, status, cor_tintura, observacoes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", agen)

        conn.commit()
        print("="*40)
        print("Carga de testes inserida com sucesso em todas as tabelas!")
        print("="*40)

    except Exception as e:
        conn.rollback()
        print(f"Ocorreu um erro durante a inserção: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_test_data()
