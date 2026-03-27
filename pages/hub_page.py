from views.hub_view import HubView, SENHA_ADMIN
from tkinter import messagebox
from model.produto import ProdutoModel
from model.cliente import ClienteModel
from model.pet import PetModel
from model.agendamento import AgendamentoModel
from model.venda import VendaModel
from model.dashboard import DashboardModel
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
        self.funcionarios = [
            (1, "Carlos (Dono)", "Proprietário", "9199999999", "carlos@petz.com", "admin", "1234"),
            (2, "Ana Costa", "Tosadora", "9188888888", "ana@petz.com", "ana.costa", "123"),
            (3, "Lucas Silva", "Veterinário", "9177777777", "lucas@petz.com", "lucas.vete", "123")
        ]

        # PDV Vendas state
        self.carrinho_cliente = None
        self.carrinho_itens = [] # format: {'tipo': 'produto'|'servico', 'id': int, 'nome': str, 'qtd': int, 'preco': float, 'id_agendamento': int(optional)}

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
        # Redireciona para o novo Dashboard
        self.tela_dashboard()

    def tela_dashboard(self):
        self.dashboard_data = {
            'estoque': DashboardModel.resumo_estoque(),
            'vendas': DashboardModel.resumo_vendas(),
            'top_produtos': DashboardModel.top_produtos_vendidos(),
            'top_servicos': DashboardModel.top_servicos_vendidos(),
            'agendamentos': DashboardModel.resumo_agendamentos(),
            'clientes': DashboardModel.resumo_clientes(),
            'vendas_7dias': DashboardModel.vendas_ultimos_7dias(),
        }
        self.view.desenhar_tela_dashboard(self.dashboard_data)
        
    def tela_registro_venda(self):
        # The new POS system logic 
        self.carregar_produtos()
        self.carregar_clientes()
        self.view.desenhar_tela_registro_venda()

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
                
    # GESTÃO DE EQUIPE ------------------------------------------
    def salvar_funcionario(self, id_func, nome, cargo, tel, email, login, senha):
        # Aqui você implementaria o FuncionarioModel.inserir ou atualizar
        # Para fins de interface imediata, vamos atualizar a lista local:
        novo_func = (id_func or len(self.funcionarios)+1, nome, cargo, tel, email, login, senha)
        
        # Simulação de salvamento (Já que não podemos alterar o banco agora)
        if id_func is None:
            self.funcionarios.append(novo_func)
        else:
            # Lógica para substituir na lista local
            pass 
            
        messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso!")
        self.tela_funcionarios()
        return True
    
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

    # LOGICA PDV / NOVA VENDA
    def buscar_servicos_nao_pagos(self, id_cliente):
        return AgendamentoModel.listar_concluidos_nao_pagos(id_cliente)

    def fechar_venda(self):
        if not self.carrinho_cliente:
            messagebox.showwarning("Aviso", "Selecione um cliente para a venda.")
            return

        if not self.carrinho_itens:
            messagebox.showwarning("Aviso", "Adicione itens ao carrinho.")
            return

        total = sum(item['preco'] * item['qtd'] for item in self.carrinho_itens)
        
        sucesso = VendaModel.finalizar_venda(self.carrinho_cliente['id'], self.carrinho_itens, total)
        if sucesso:
            # Stats fallbacks for old Dashboard 
            for it in self.carrinho_itens:
                if it['tipo'] == 'produto' and it['nome'] in self.vendas_produtos:
                    self.vendas_produtos[it['nome']] += it['qtd']
                elif it['tipo'] == 'servico' and it['nome'] in self.vendas_servicos:
                    self.vendas_servicos[it['nome']] += it['qtd']
                    
            messagebox.showinfo("Venda Finalizada", f"Venda nº finalizada com sucesso!\nTotal: R$ {total:.2f}")
            self.carrinho_cliente = None
            self.carrinho_itens = []
            self.tela_registro_venda()  # Refresh the screen
        else:
            messagebox.showerror("Erro", "Falha ao registrar venda.")
