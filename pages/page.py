from tkinter import messagebox
from views.view import LoginView, SetupView
from model.database import get_connection

class LoginPage:
    def __init__(self, master, on_login_success=None):
        self.master = master
        self.on_login_success = on_login_success
        
        # Check if we have any employees
        conn = get_connection()
        total_funcionarios = 0
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM FUNCIONARIO")
                    total_funcionarios = cursor.fetchone()[0]
            except Exception as e:
                print(f"Erro ao verificar funcionários: {e}")
            finally:
                conn.close()
                pass

        if total_funcionarios == 0:
            self.view = SetupView(master=self.master, on_setup_click=self.tentar_setup)
        else:
            self.view = LoginView(master=self.master, on_login_click=self.tentar_login)
            
        self.view.place(relx=0.5, rely=0.5, anchor="center")
        
    def tentar_setup(self, nome, login, email, senha):
        if not nome or not login or not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios.")
            return

        conn = get_connection()
        if not conn: return
        
        try:
            with conn.cursor() as cursor:
                # O primeiro funcionário é obrigatoriamente um Dono
                cursor.execute(
                    "INSERT INTO FUNCIONARIO (nome, cargo, telefone, email, login, senha) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nome, "Dono", "", email, login, senha)
                )
                novo_id = cursor.lastrowid
            conn.commit()
            
            messagebox.showinfo("Sucesso", f"Sistema configurado com sucesso!\nBem-vindo(a), {nome}.")
            funcionario = (novo_id, nome, "Dono")
            if self.on_login_success:
                self.on_login_success(funcionario)
                
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao configurar sistema: {e}")
        finally:
            conn.close()
        
    def tentar_login(self, email, senha):
        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha o e-mail e a senha.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Erro", "Erro ao conectar com o banco de dados 'caobalhota'.\nVerifique se o servidor MySQL está rodando.")
            return

        try:
            cursor = conn.cursor()
            sql = "SELECT id, nome, cargo FROM FUNCIONARIO WHERE email = %s AND senha = %s"
            cursor.execute(sql, (email, senha))
            funcionario = cursor.fetchone()

            if funcionario:
                nome_func = funcionario[1]
                cargo_func = funcionario[2]
                messagebox.showinfo("Sucesso", f"Login realizado com sucesso!\nBem-vindo(a), {nome_func}.")
                if self.on_login_success:
                    self.on_login_success(funcionario)
            else:
                messagebox.showerror("Acesso Negado", "E-mail ou senha incorretos.")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao realizar o login:\n{e}")
        finally:
            conn.close()
