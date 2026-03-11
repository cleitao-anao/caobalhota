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
