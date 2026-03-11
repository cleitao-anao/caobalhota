import customtkinter as ctk
from pages.page import LoginPage
from pages.hub_page import HubPage

# Configuracoes de cor para fundo
COR_FUNDO_EXTERNO = "#F3F6F8"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Cãobalhota - Pro System")
        self.geometry("1200x800") 
        self.resizable(False, False)
        self.configure(fg_color=COR_FUNDO_EXTERNO)

        # Inicia pela tela de login
        self.show_login()

    def show_login(self):
        self.login_page = LoginPage(self, on_login_success=self.show_hub)

    def show_hub(self):
        # Destruir a tela de login
        self.login_page.view.place_forget()
        self.login_page.view.destroy()
        
        # Mudar a cor de fundo caso a pagina de login force alguma, mas ja foi configurada em init
        
        # Montar a pagina do hub
        self.hub_page = HubPage(self)
        self.hub_page.mount()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
