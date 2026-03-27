import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_click, **kwargs):
        super().__init__(master, width=320, height=360, corner_radius=15, **kwargs)
        
        self.on_login_click = on_login_click
        
        # Título
        self.label_titulo = ctk.CTkLabel(master=self, text="Cãobalhota - Login", font=("Roboto", 24, "bold"))
        self.label_titulo.place(relx=0.5, rely=0.15, anchor="center")

        # Campo de E-mail
        self.email_entry = ctk.CTkEntry(master=self, width=250, placeholder_text="E-mail")
        self.email_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Campo de Senha
        self.senha_entry = ctk.CTkEntry(master=self, width=250, placeholder_text="Senha", show="*")
        self.senha_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Botão
        self.btn_login = ctk.CTkButton(master=self, width=250, text="Entrar", corner_radius=6, 
                                       command=self._handle_login)
        self.btn_login.place(relx=0.5, rely=0.75, anchor="center")

    def _handle_login(self):
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        self.on_login_click(email, senha)

class SetupView(ctk.CTkFrame):
    def __init__(self, master, on_setup_click, **kwargs):
        super().__init__(master, width=380, height=450, corner_radius=15, **kwargs)
        
        self.on_setup_click = on_setup_click
        
        # Título
        self.label_titulo = ctk.CTkLabel(master=self, text="Bem-vindo ao Cãobalhota", font=("Roboto", 22, "bold"))
        self.label_titulo.place(relx=0.5, rely=0.1, anchor="center")
        
        self.label_sub = ctk.CTkLabel(master=self, text="Configure a conta de Dono (1º acesso)", font=("Roboto", 12), text_color="gray")
        self.label_sub.place(relx=0.5, rely=0.18, anchor="center")

        # Campo de Nome
        self.nome_entry = ctk.CTkEntry(master=self, width=280, placeholder_text="Seu Nome *")
        self.nome_entry.place(relx=0.5, rely=0.32, anchor="center")

        # Campo de Login
        self.login_entry = ctk.CTkEntry(master=self, width=280, placeholder_text="Login de acesso *")
        self.login_entry.place(relx=0.5, rely=0.45, anchor="center")

        # Campo de E-mail
        self.email_entry = ctk.CTkEntry(master=self, width=280, placeholder_text="E-mail *")
        self.email_entry.place(relx=0.5, rely=0.58, anchor="center")

        # Campo de Senha
        self.senha_entry = ctk.CTkEntry(master=self, width=280, placeholder_text="Senha *", show="*")
        self.senha_entry.place(relx=0.5, rely=0.71, anchor="center")

        # Botão
        self.btn_setup = ctk.CTkButton(master=self, width=280, text="Cadastrar e Entrar", corner_radius=6, 
                                       command=self._handle_setup, fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_setup.place(relx=0.5, rely=0.88, anchor="center")

    def _handle_setup(self):
        nome = self.nome_entry.get().strip()
        login = self.login_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        self.on_setup_click(nome, login, email, senha)
