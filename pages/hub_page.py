from views.hub_view import HubView
from tkinter import messagebox
from model.produto import ProdutoModel
from model.cliente import ClienteModel
from model.pet import PetModel
from model.agendamento import AgendamentoModel
from model.venda import VendaModel
from model.dashboard import DashboardModel
from model.servico import ServicoModel
# Mapa de permissões de AÇÃO por cargo
# Todos os funcionários podem VER todas as telas
# Apenas os cargos listados podem ALTERAR/AGIR nas áreas especificadas
PERMISSAO_POR_CARGO = {
    'Dono': ['estoque_editar', 'equipe_editar', 'caixa', 'cadastrar', 'clientes_editar', 'agenda_editar', 'servicos_editar'],
    'Repositor': ['estoque_editar'],
    'Caixa': ['caixa', 'agenda_editar'],
    'Atendente': ['cadastrar', 'clientes_editar', 'agenda_editar'],
    'Veterinário': ['agenda_editar'],
    'Veterinario': ['agenda_editar'],
    'Esteticista': ['agenda_editar'],
}

class HubPage:
    def __init__(self, master, funcionario_data=None):
        self.master = master
        
        # Dados do funcionário logado
        if funcionario_data:
            self.funcionario_logado = {
                'id': funcionario_data[0],
                'nome': funcionario_data[1],
                'cargo': funcionario_data[2]
            }
        else:
            self.funcionario_logado = {'id': 0, 'nome': 'Usuário', 'cargo': 'Atendente'}
        
        self.vendas_produtos = {p: 0 for p in ["Ração", "Shampoo", "Coleira", "Petisco", "Brinquedo", "Cama", "Roupas", "Osso", "Caixa", "Escova"]}
        self.vendas_servicos = {s: 0 for s in ["Tosa", "Banho", "Hidratação", "Unhas", "Ouvidos", "Taxi Pet", "Hospedagem", "Adestramento", "Consulta", "Vacina"]}
        # Real product list from DB
        self.produtos = []
        self.servicos = []
        self.clientes = []
        self.agendamentos = [] 
        self.funcionarios = [
            (1, "Carlos (Dono)", "Proprietário", "9199999999", "carlos@petz.com", "admin", "1234"),
            (2, "Ana Costa", "Tosadora", "9188888888", "ana@petz.com", "ana.costa", "123"),
            (3, "Lucas Silva", "Veterinário", "9177777777", "lucas@petz.com", "lucas.vete", "123")
        ]

        # PDV Vendas state
        self.carrinho_cliente = None
        self.carrinho_itens = []

        self.view = HubView(master, self)
        
    def pack(self, **kwargs):
        self.view.pack(**kwargs)

    def mount(self):
        """Called to display the page."""
        self.pack(fill="both", expand=True)
        self.mostrar_controle()

    def tem_permissao(self, area):
        """Verifica se o funcionário logado tem permissão para acessar a área."""
        cargo = self.funcionario_logado.get('cargo', '')
        permissoes = PERMISSAO_POR_CARGO.get(cargo, [])
        return area in permissoes

    def verificar_acesso(self, area, nome_tela="esta tela"):
        """Verifica acesso e exibe aviso se negado. Retorna True se permitido."""
        if not self.tem_permissao(area):
            cargo = self.funcionario_logado.get('cargo', 'Desconhecido')
            messagebox.showwarning("Acesso Negado", f"O cargo '{cargo}' não tem permissão para acessar {nome_tela}.")
            return False
        return True

    def sair_trocar_usuario(self):
        """Volta para a tela de login."""
        self.view.pack_forget()
        self.view.destroy()
        self.master.show_login()

    def mostrar_controle(self):
        self.view.desenhar_controle()

    def tela_registros(self):
        self.carregar_produtos()
        self.carregar_servicos()
        self.view.desenhar_tela_registros()

    def tela_estoque_visualizacao(self):
        self.carregar_produtos()
        self.view.desenhar_tela_estoque_visualizacao()

    def tela_funcionarios(self):
        self.view.desenhar_tela_funcionarios()

    def tela_servicos(self):
        self.carregar_servicos()
        self.view.desenhar_tela_servicos()

    def carregar_servicos(self):
        self.servicos = ServicoModel.listar_todos()

    def tela_agenda(self):
        self.agendamentos = AgendamentoModel.listar_todos()
        self.view.desenhar_tela_agenda()

    def criar_agendamento(self, id_cliente, id_pet, id_servico, id_funcionario, data, hora, cor_tintura='', observacoes=''):
        sucesso = AgendamentoModel.inserir(id_cliente, id_pet, id_servico, id_funcionario, data, hora, cor_tintura, observacoes)
        if sucesso:
            messagebox.showinfo("Sucesso", "Agendamento criado com sucesso!")
            self.tela_agenda()
            return True
        else:
            messagebox.showerror("Erro", "Erro ao criar agendamento.")
            return False

    def atualizar_status_agendamento(self, id_agendamento, novo_status):
        sucesso = AgendamentoModel.atualizar_status(id_agendamento, novo_status)
        if sucesso:
            messagebox.showinfo("Sucesso", f"Status atualizado para '{novo_status}'!")
            self.tela_agenda()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar status.")

    def salvar_servico(self, id_servico_atual, nome, valor_base, descricao):
        try:
            valor_float = float(valor_base.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Aviso", "O valor base deve ser numérico.")
            return False

        if not nome or valor_float < 0:
            messagebox.showwarning("Aviso", "Nome não pode ser vazio. Valor não pode ser negativo.")
            return False

        if id_servico_atual is None:
            sucesso = ServicoModel.inserir(nome, valor_float, descricao)
            msg = "cadastrado"
        else:
            sucesso = ServicoModel.atualizar(id_servico_atual, nome, valor_float, descricao)
            msg = "atualizado"

        if sucesso:
            messagebox.showinfo("Sucesso", f"Serviço {msg} com sucesso!")
            self.tela_servicos()
            return True
        else:
            messagebox.showerror("Erro", "Erro ao salvar serviço no banco de dados.")
            return False

    def excluir_servico(self, id_servico):
        if not self.verificar_acesso('servicos_editar', 'gerenciar Serviços'): return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este serviço?"):
            if ServicoModel.deletar(id_servico):
                messagebox.showinfo("Sucesso", "Serviço excluído com sucesso.")
                self.tela_servicos()
            else:
                messagebox.showerror("Erro", "Erro ao excluir o serviço.")

    def tela_vendas(self):
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
        self.carregar_produtos()
        self.carregar_clientes()
        self.view.desenhar_tela_registro_venda()

    def carregar_clientes(self):
        self.clientes = ClienteModel.listar_todos()

    def tela_cadastro(self):
        self.carregar_clientes()
        self.view.desenhar_tela_cadastro()

    def tela_pets_cliente(self, cliente):
        self.view.desenhar_tela_pets_cliente(cliente)

    def excluir_cliente_logica(self, id_cliente):
        if not self.verificar_acesso('clientes_editar', 'editar Clientes'): return
        if messagebox.askyesno("Confirmar", "Deseja excluir este cliente e todos os seus pets?"):
            if ClienteModel.deletar(id_cliente):
                messagebox.showinfo("Sucesso", "Cliente excluído!")
                self.tela_cadastro()
            else:
                messagebox.showerror("Erro", "Falha ao excluir cliente.")

    def excluir_pet_logica(self, cliente, id_pet):
        if not self.verificar_acesso('clientes_editar', 'editar Pets'): return
        if messagebox.askyesno("Confirmar", "Deseja excluir este pet?"):
            if PetModel.deletar(id_pet):
                messagebox.showinfo("Sucesso", "Pet excluído!")
                self.tela_pets_cliente(cliente)
            else:
                messagebox.showerror("Erro", "Falha ao excluir pet.")

    def abrir_modal_cadastro(self, item_para_venda=None, tipo_venda=None):
        if not self.verificar_acesso('cadastrar', 'Cadastro de Clientes'): return
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
        if not self.verificar_acesso('equipe_editar', 'gerenciar Equipe'): return
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
        if not self.verificar_acesso('caixa', 'finalizar Vendas'): return
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
