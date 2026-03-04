from views.hub_view import HubView, SENHA_ADMIN
from tkinter import messagebox

class HubPage:
    def __init__(self, master):
        self.master = master
        
        # State from original Hub
        self.is_admin = False
        self.vendas_produtos = {p: 0 for p in ["Ração", "Shampoo", "Coleira", "Petisco", "Brinquedo", "Cama", "Roupas", "Osso", "Caixa", "Escova"]}
        self.vendas_servicos = {s: 0 for s in ["Tosa", "Banho", "Hidratação", "Unhas", "Ouvido", "Taxi Pet", "Hospedagem", "Adestramento", "Consulta", "Vacina"]}
        self.estoque_produtos = {p: 50 for p in self.vendas_produtos.keys()}
        self.clientes_cadastrados = []
        self.agendamentos = [] 
        self.funcionarios = ["Carlos  (Dono)", "Ana Costa", "Lucas "]

        self.view = HubView(master, self)
        
    def pack(self, **kwargs):
        self.view.pack(**kwargs)

    def mount(self):
        """Called to display the page."""
        self.pack(fill="both", expand=True)
        self.mostrar_controle()

    def solicitar_senha_admin(self):
        if self.is_admin:
            self.is_admin = False
            self.view.set_admin_button_state(False)
            self.mostrar_controle()
            return
        
        senha = self.view.pedir_senha_admin()
        try:
            if senha == SENHA_ADMIN:
                self.is_admin = True
                self.view.set_admin_button_state(True)
                messagebox.showinfo("Sucesso", "Modo Administrador!")
                self.mostrar_controle()
            elif senha is not None:
                messagebox.showerror("Erro", "Incorreta!")
        except Exception:
            pass

    def mostrar_controle(self):
        self.view.desenhar_controle()

    def tela_registros(self):
        self.view.desenhar_tela_registros()

    def tela_estoque_visualizacao(self):
        self.view.desenhar_tela_estoque_visualizacao()

    def tela_funcionarios(self):
        self.view.desenhar_tela_funcionarios()

    def tela_vendas(self):
        self.view.desenhar_tela_vendas()

    def tela_agenda(self):
        self.view.desenhar_tela_agenda()

    def abrir_modal_cadastro(self, item_para_venda=None, tipo_venda=None):
        self.view.abrir_modal_cadastro(item_para_venda, tipo_venda)

    def alterar_estoque(self, p, v):
        self.estoque_produtos[p] += v
        self.tela_estoque_visualizacao()

    def demitir_funcionario(self, func):
        if func in self.funcionarios:
            self.funcionarios.remove(func)
        self.tela_funcionarios()

    def finalizar_venda_logica(self, item, tipo, cliente=None, data_hora=None):
        if tipo == "produto":
            self.vendas_produtos[item] += 1
            self.estoque_produtos[item] -= 1
        else:
            self.vendas_servicos[item] += 1
            if cliente:
                info_servico = f"{item} ({data_hora})" if data_hora else item
                self.agendamentos.append({"humano": cliente['humano'], "pet": cliente['pet'], "servico": info_servico})
        messagebox.showinfo("Sucesso", f"{item} concluído!")
