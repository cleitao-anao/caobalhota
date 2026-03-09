from model.database import get_connection

def insert_test_data():
    conn = get_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        
        # Dados de teste para Funcionario
        funcionarios = [
            ("João Silva", "Veterinário", "11999999999", "joao@caobalhota.com", "joao.silva", "123456"),
            ("Maria Oliveira", "Recepcionista", "11988888888", "maria@caobalhota.com", "maria.oliveira", "senha123"),
            ("Admin Teste", "Administrador", "11000000000", "admin@teste.com", "admin", "admin")
        ]
        
        # Insere os dados
        sql = "INSERT INTO FUNCIONARIO (nome, cargo, telefone, email, login, senha) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Verifica se os usuários já existem para não dar erro de UNIQUE no login
        cursor.execute("SELECT login FROM FUNCIONARIO")
        logins_existentes = [row[0] for row in cursor.fetchall()]

        inseridos = 0
        for func in funcionarios:
            if func[4] not in logins_existentes: # func[4] é o login
                cursor.execute(sql, func)
                inseridos += 1
        
        # Comita as transações se houver inserções
        if inseridos > 0:
            conn.commit()
            print(f"Sucesso! {inseridos} funcionários de teste inseridos no banco 'caobalhota'.")
            print("Você pode testar o login com os seguintes e-mails e senhas:")
            print("1. E-mail: admin@teste.com | Senha: admin")
            print("2. E-mail: joao@caobalhota.com | Senha: 123456")
            print("3. E-mail: maria@caobalhota.com | Senha: senha123")
        else:
            print("Os usuários de teste já existem no banco de dados.")
            print("Tente fazer login com: E-mail: admin@teste.com | Senha: admin")

    except Exception as e:
        # Se ocorrer erro, faz o rollback
        conn.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_test_data()
