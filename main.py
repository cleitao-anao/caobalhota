import customtkinter as ctk
from pages.page import LoginPage

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Sistema Cãobalhota")
    app.geometry("600x450")
    
    # Instancia e exibe a página de login
    login_page = LoginPage(app)

    app.mainloop()

if __name__ == "__main__":
    main()
