from views.hub_view import HubView, SENHA_ADMIN
from tkinter import messagebox
from model.produto import ProdutoModel
from model.cliente import ClienteModel
from model.pet import PetModel
class HubPage:
    def __init__(self, master):
        self.master = master
        
        # State from original Hub
        self.is_admin = False
        self.vendas_produtos = {p: 0 for p in ["Ração", "Shampoo", "Coleira", "Petisco", "Brinquedo", "Cama", "Roupas", "Osso", "Caixa", "Escova"]}
        self.vendas_servicos = {s: 0 for s in ["Tosa", "Banho", "Hidratação", "Unhas", "Ouvidos", "Taxi Pet", "Hospedagem", "Adestramento", "Consulta", "Vacina"]}
        # Real product list from DB
        self.produtos = []
        self.clientes = []  # Array of tuples: (id, nome, cpf, telefone, email, endereco, admin)
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
        # Update logic to pass current inventory list if necessary
        self.carregar_produtos()
        self.view.desenhar_tela_registros()

    def tela_estoque_visualizacao(self):
        self.carregar_produtos()
        self.view.desenhar_tela_estoque_visualizacao()

    def tela_funcionarios(self):
        self.view.desenhar_tela_funcionarios()

    def tela_vendas(self):
        self.view.desenhar_tela_vendas()

    def tela_agenda(self):
        self.view.desenhar_tela_agenda()

    def carregar_clientes(self):
        self.clientes = ClienteModel.listar_todos()

    def tela_cadastro(self):
        self.carregar_clientes()
        self.view.desenhar_tela_cadastro()

    def tela_pets_cliente(self, cliente):
        self.view.desenhar_tela_pets_cliente(cliente)

    def excluir_cliente_logica(self, id_cliente):
        if messagebox.askyesno("Confirmar", "Deseja excluir este cliente e todos os seus pets?"):
            if ClienteModel.deletar(id_cliente):
                messagebox.showinfo("Sucesso", "Cliente excluído!")
                self.tela_cadastro()
            else:
                messagebox.showerror("Erro", "Falha ao excluir cliente.")

    def excluir_pet_logica(self, cliente, id_pet):
        if messagebox.askyesno("Confirmar", "Deseja excluir este pet?"):
            if PetModel.deletar(id_pet):
                messagebox.showinfo("Sucesso", "Pet excluído!")
                self.tela_pets_cliente(cliente)
            else:
                messagebox.showerror("Erro", "Falha ao excluir pet.")

    def abrir_modal_cadastro(self, item_para_venda=None, tipo_venda=None):
        self.view.abrir_modal_cadastro(item_para_venda, tipo_venda)

    def salvar_cliente_com_pet(self, dados):
        # dados is a dict from hub_view matching the old format: {"humano": "", "cpf": "", "telefone": "", "endereco": "", "email": "", "pets": [{nome, especie, raca, idade, porte, cuidados_especiais}]}
        id_cliente = ClienteModel.inserir(dados['humano'], dados['cpf'], dados['telefone'], dados.get('email', ''), dados['endereco'])
        if id_cliente:
            for p in dados.get('pets', []):
                PetModel.inserir(id_cliente, p['nome'], p['especie'], p['raca'], p['idade'], p.get('porte', ''), p.get('cuidados_especiais', ''))
            return id_cliente
        return None

    # CRUD DE PRODUTO ------------------------------------------
    def carregar_produtos(self):
        self.produtos = ProdutoModel.listar_todos()

    def alterar_estoque(self, id_produto, qtd_alteracao):
        produto = ProdutoModel.buscar_por_id(id_produto)
        if produto:
            novo_estoque = produto[5] + qtd_alteracao
            if novo_estoque < 0: novo_estoque = 0 # Previne estoque negativo
            sucesso = ProdutoModel.atualizar(produto[0], produto[1], produto[2], produto[3], produto[4], novo_estoque)
            if sucesso:
                self.tela_estoque_visualizacao()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar estoque no banco de dados.")

    def salvar_produto(self, id_produto_atual, codigo, nome, descricao, preco, estoque):
        try:
            preco_float = float(preco.replace(",", "."))
            estoque_int = int(estoque)
        except ValueError:
            messagebox.showwarning("Aviso", "Preço e Estoque devem ser numéricos.")
            return False

        if not nome or preco_float < 0 or estoque_int < 0:
            messagebox.showwarning("Aviso", "Nome não pode ser vazio. Valores não podem ser negativos.")
            return False

        if id_produto_atual is None:
            # INSERIR
            sucesso = ProdutoModel.inserir(codigo, nome, descricao, preco_float, estoque_int)
            msg = "cadastrado"
        else:
            # ATUALIZAR
            sucesso = ProdutoModel.atualizar(id_produto_atual, codigo, nome, descricao, preco_float, estoque_int)
            msg = "atualizado"

        if sucesso:
            messagebox.showinfo("Sucesso", f"Produto {msg} com sucesso!")
            self.tela_estoque_visualizacao()
            return True
        else:
            messagebox.showerror("Erro", f"Erro ao salvar produto no banco de dados.")
            return False

    def excluir_produto(self, id_produto):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            if ProdutoModel.deletar(id_produto):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
                self.tela_estoque_visualizacao()
            else:
                messagebox.showerror("Erro", "Erro ao excluir o produto.")
    
    # OUTROS ----------------------------------------------------

    def demitir_funcionario(self, func):
        if func in self.funcionarios:
            self.funcionarios.remove(func)
        self.tela_funcionarios()

    def finalizar_venda_logica(self, item, tipo, cliente=None, data_hora=None):
        if tipo == "produto":
            pass # A logica antiga do PDV dependia da lista fake. Requeriria DB em VENDA e ITEM_VENDA futuramente.
            # self.vendas_produtos[item] += 1
            # self.estoque_produtos[item] -= 1
        else:
            self.vendas_servicos[item] += 1
            if cliente:
                pets_str = ", ".join(p.get("nome", "") for p in cliente.get("pets", [])) if "pets" in cliente else cliente.get("pet", "Desconhecido")
                info_servico = f"{item} ({data_hora})" if data_hora else item
                self.agendamentos.append({"humano": cliente.get('humano', ''), "pet": pets_str, "servico": info_servico})
        messagebox.showinfo("Sucesso", f"{item} concluído!")
