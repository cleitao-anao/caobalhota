import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry 

# =================================================================
# gerais cores 
# =================================================================
COR_FUNDO_EXTERNO   = "#F3F6F8"
COR_NAVBAR          = "#00539F"
COR_ACCENT          = "#FFD100"
COR_CARD            = "#FFFFFF"
COR_BORDA           = "#E0E0E0"
COR_TEXTO_NAV       = "#FFFFFF"
COR_TEXTO_TITULO    = "#333333"
COR_TEXTO_PADRAO    = "#555555"
COR_INPUT_BG        = "#FFFFFF"
COR_INPUT_TEXTO     = "#000000"
COR_BOTAO_SALVAR    = "#00539F"
COR_BOTAO_ACCENT    = "#FFD100"
COR_BOTAO_HOVER     = "#004080"
COR_BOTAO_VOLTAR    = "#333333"
COR_SUCESSO         = "#28A745"
COR_PERIGO          = "#DC3545"

SENHA_ADMIN         = "1234" 

class HubView(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color=COR_FUNDO_EXTERNO, **kwargs)
        self.controller = controller

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.navbar = ctk.CTkFrame(self.main_container, fg_color=COR_NAVBAR, height=80, corner_radius=0)
        self.navbar.pack(fill="x")
        self.navbar.pack_propagate(False)
        
        logo_frame = ctk.CTkFrame(self.navbar, fg_color=COR_BOTAO_ACCENT, width=60, height=40, corner_radius=8)
        logo_frame.pack(side="left", padx=(30, 10))
        ctk.CTkLabel(logo_frame, text="🐶", font=("Inter", 20), text_color="#000").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.navbar, text="CÃOBALHOTA", font=("Inter", 24, "bold"), text_color=COR_TEXTO_NAV).pack(side="left")

        self.btn_admin = ctk.CTkButton(self.navbar, text="🔓 Admin", width=100, height=35, 
                                       fg_color="transparent", border_width=1, border_color=COR_TEXTO_NAV,
                                       hover_color=COR_BOTAO_HOVER, command=self.controller.solicitar_senha_admin)
        self.btn_admin.pack(side="right", padx=30)

        self.nav_btns = ctk.CTkFrame(self.navbar, fg_color="transparent")
        self.nav_btns.pack(side="right", padx=10)

        opts = {"fg_color": "transparent", "text_color": COR_TEXTO_NAV, "hover_color": COR_BOTAO_HOVER, "corner_radius": 20, "width": 110, "font": ("Inter", 13, "bold")}
        ctk.CTkButton(self.nav_btns, text="Dashboard", command=self.controller.mostrar_controle, **opts).pack(side="left", padx=5)
        ctk.CTkButton(self.nav_btns, text="Cadastrar", command=self.controller.abrir_modal_cadastro, **opts).pack(side="left", padx=5)
        ctk.CTkButton(self.nav_btns, text="🛒 Loja Petz", command=self.controller.tela_registros, **opts).pack(side="left", padx=5)

        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=30, pady=20)

    def set_admin_button_state(self, is_admin):
        if is_admin:
            self.btn_admin.configure(text="🔒 Ativo", fg_color=COR_BOTAO_ACCENT, text_color="#000")
        else:
            self.btn_admin.configure(text="🔓 Admin", fg_color="transparent")

    def pedir_senha_admin(self):
        dialog = ctk.CTkInputDialog(text="Senha Admin:", title="Acesso")
        return dialog.get_input()

    def limpar_tela(self):
        for widget in self.content_area.winfo_children(): widget.destroy()

    def desenhar_controle(self):
        self.limpar_tela()
        banner = ctk.CTkFrame(self.content_area, fg_color=COR_BOTAO_ACCENT, height=120, corner_radius=20)
        banner.pack(fill="x", pady=(0, 30))
        ctk.CTkLabel(banner, text="Olá! O que vamos fazer hoje? 🐾", font=("Inter", 22, "bold"), text_color="#000").place(relx=0.05, rely=0.5, anchor="w")

        grid = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid.pack(expand=True, fill="both")
        
        menu = [("AGENDA", "📅", self.controller.tela_agenda), ("ESTOQUE", "📦", self.controller.tela_estoque_visualizacao), ("EQUIPE", "👥", self.controller.tela_funcionarios), ("RELATÓRIOS", "📊", self.controller.tela_vendas)]
        
        for i, (t, icon, cmd) in enumerate(menu):
            f = ctk.CTkFrame(grid, fg_color=COR_CARD, corner_radius=20, border_width=1, border_color=COR_BORDA)
            f.grid(row=0, column=i, padx=15, sticky="nsew")
            grid.columnconfigure(i, weight=1)
            ctk.CTkLabel(f, text=icon, font=("Inter", 50)).pack(pady=(40, 10))
            ctk.CTkLabel(f, text=t, font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack()
            ctk.CTkButton(f, text="Acessar", command=cmd, fg_color=COR_NAVBAR, corner_radius=15, width=120).pack(pady=30)

    def criar_input(self, master, placeholder):
        ent = ctk.CTkEntry(master, placeholder_text=placeholder, fg_color="#F9F9F9", border_color=COR_BORDA, text_color=COR_INPUT_TEXTO, height=45)
        ent.pack(fill="x", pady=5, padx=10)
        return ent

    def abrir_modal_cadastro(self, item_para_venda=None, tipo_venda=None):
        modal = ctk.CTkToplevel(self)
        modal.geometry("600x750")
        modal.title("Novo Cadastro")
        modal.configure(fg_color=COR_FUNDO_EXTERNO)
        modal.attributes("-topmost", True)
        modal.grab_set()

        scroll = ctk.CTkScrollableFrame(modal, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        scroll.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(scroll, text="👤 Informações do Cliente", font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=10, anchor="w", padx=10)
        ent_nome = self.criar_input(scroll, "Nome Completo")
        ent_cpf = self.criar_input(scroll, "CPF")
        ent_tel = self.criar_input(scroll, "Telefone")
        ent_end = self.criar_input(scroll, "Endereço")

        ctk.CTkLabel(scroll, text="🐾 Informações do Pet", font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=(20,10), anchor="w", padx=10)
        ent_pet_nome = self.criar_input(scroll, "Nome do Pet")
        
        def on_especie_change(escolha):
            if escolha == "Outro": ent_custom.pack(fill="x", pady=5, padx=10)
            else: ent_custom.pack_forget()

        ent_especie = ctk.CTkOptionMenu(scroll, values=["Cão", "Gato", "Pássaro", "Outro"], 
                                        command=on_especie_change, fg_color="#F0F0F0", text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        ent_especie.pack(fill="x", pady=5, padx=10)
        
        ent_custom = ctk.CTkEntry(scroll, placeholder_text="Qual espécie?", fg_color=COR_INPUT_BG, text_color=COR_INPUT_TEXTO)
        
        ent_raca = self.criar_input(scroll, "Raça")
        ent_idade = self.criar_input(scroll, "Idade")

        def salvar():
            esp = ent_custom.get() if ent_especie.get() == "Outro" else ent_especie.get()
            if not ent_nome.get() or not ent_pet_nome.get():
                messagebox.showwarning("Atenção", "Preencha os campos obrigatórios!")
                return
            dados = {"humano": ent_nome.get(), "pet": ent_pet_nome.get(), "especie": esp}
            self.controller.clientes_cadastrados.append(dados)
            modal.destroy()
            if item_para_venda: 
                if tipo_venda == "servico":
                    self.abrir_modal_data_hora(item_para_venda, dados)
                else:
                    self.controller.finalizar_venda_logica(item_para_venda, tipo_venda, cliente=dados)
            messagebox.showinfo("Petz", f"Bem-vindo(a), {ent_nome.get()}!")

        ctk.CTkButton(modal, text="Finalizar Cadastro", fg_color=COR_BOTAO_ACCENT, text_color="#000", font=("Inter", 14, "bold"), height=50, command=salvar).pack(pady=20)

    def desenhar_tela_registros(self):
        self.limpar_tela()
        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        ctk.CTkLabel(scroll, text="📦 Melhores Ofertas", font=("Inter", 22, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=(0, 15), anchor="w")
        gp = ctk.CTkFrame(scroll, fg_color="transparent")
        gp.pack(fill="x")
        for i, p_row in enumerate(self.controller.produtos):
            # p_row format: (id, codigo, nome, descricao, preco, estoque)
            p_id = p_row[0]
            p_nome = p_row[2]
            p_estoque = p_row[5]
            
            card = ctk.CTkFrame(gp, fg_color=COR_CARD, corner_radius=12, border_width=1, border_color=COR_BORDA, width=180, height=120)
            card.grid(row=i//5, column=i%5, padx=8, pady=8)
            card.grid_propagate(False)
            
            ctk.CTkLabel(card, text=p_nome, font=("Inter", 13, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=(15, 0))
            ctk.CTkLabel(card, text=f"Estoque: {p_estoque}", font=("Inter", 11), text_color="gray").pack()
            ctk.CTkButton(card, text="Comprar", height=28, width=100, fg_color=COR_NAVBAR, 
                          command=lambda x=p_nome: self.fluxo_venda(x, "produto")).pack(pady=10)

        ctk.CTkLabel(scroll, text="✂️ Centro de Estética & Saúde (Obrigatório Cadastro)", font=("Inter", 22, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=(30, 15), anchor="w")
        gs = ctk.CTkFrame(scroll, fg_color="transparent")
        gs.pack(fill="x")
        for i, s in enumerate(self.controller.vendas_servicos.keys()):
            card = ctk.CTkFrame(gs, fg_color=COR_NAVBAR, corner_radius=12, width=180, height=100)
            card.grid(row=i//5, column=i%5, padx=8, pady=8)
            card.grid_propagate(False)
            ctk.CTkLabel(card, text=s, font=("Inter", 13, "bold"), text_color=COR_TEXTO_NAV).pack(expand=True)
            ctk.CTkButton(card, text="Agendar", fg_color=COR_BOTAO_ACCENT, text_color="#000", height=25, width=120, font=("Inter", 11, "bold"),
                          command=lambda x=s: self.fluxo_venda(x, "servico")).pack(pady=(0, 15))

    def fluxo_venda(self, item, tipo):
        pop = ctk.CTkToplevel(self)
        pop.geometry("450x580")
        pop.title("Check-out")
        pop.configure(fg_color=COR_FUNDO_EXTERNO)
        pop.attributes("-topmost", True)
        pop.grab_set()

        ctk.CTkLabel(pop, text=f"🛒 {item}", font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        container_busca = ctk.CTkFrame(pop, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        container_busca.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(container_busca, text="Localizar Cadastro", font=("Inter", 14, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=10)
        busca_ent = ctk.CTkEntry(container_busca, placeholder_text="🔍 Nome do cliente...", fg_color="#F0F0F0", border_width=0, text_color=COR_INPUT_TEXTO)
        busca_ent.pack(fill="x", padx=20, pady=5)

        lista_busca = ctk.CTkScrollableFrame(container_busca, fg_color="transparent", height=180)
        lista_busca.pack(fill="both", expand=True, padx=10, pady=10)

        def atualizar_busca(event=None):
            for w in lista_busca.winfo_children(): w.destroy()
            termo = busca_ent.get().lower()
            for c in self.controller.clientes_cadastrados:
                if termo in c['humano'].lower():
                    f_res = ctk.CTkFrame(lista_busca, fg_color="#F9F9F9", height=40)
                    f_res.pack(fill="x", pady=2)
                    ctk.CTkLabel(f_res, text=f"{c['humano']} ({c['pet']})", text_color=COR_TEXTO_TITULO, font=("Inter", 12)).pack(side="left", padx=10)
                    ctk.CTkButton(f_res, text="Selecionar", width=80, height=24, fg_color=COR_SUCESSO, 
                                  command=lambda cl=c: [pop.destroy(), self.abrir_modal_data_hora(item, cl) if tipo == "servico" else self.controller.finalizar_venda_logica(item, tipo, cl)]).pack(side="right", padx=5)

        busca_ent.bind("<KeyRelease>", atualizar_busca)
        atualizar_busca()

        ctk.CTkButton(pop, text="+ Novo Cliente", fg_color=COR_NAVBAR, command=lambda: [pop.destroy(), self.abrir_modal_cadastro(item, tipo)]).pack(pady=5)
        
        estado_visitante = "disabled" if tipo == "servico" else "normal"
        ctk.CTkButton(pop, text="Visitante (Sem Agenda)", fg_color="transparent", border_width=1, border_color="#777", text_color=COR_TEXTO_TITULO, state=estado_visitante,
                      command=lambda: [self.controller.finalizar_venda_logica(item, tipo), pop.destroy()]).pack(pady=5)

    def abrir_modal_data_hora(self, servico, cliente):
        modal_dt = ctk.CTkToplevel(self)
        modal_dt.geometry("400x450")
        modal_dt.title("Escolher Data e Hora")
        modal_dt.attributes("-topmost", True)
        modal_dt.grab_set()

        ctk.CTkLabel(modal_dt, text=f"Agendar {servico}", font=("Inter", 18, "bold"), text_color=COR_NAVBAR).pack(pady=15)
        ctk.CTkLabel(modal_dt, text=f"Cliente: {cliente['humano']} & {cliente['pet']}", font=("Inter", 12)).pack()

        ctk.CTkLabel(modal_dt, text="Selecione a Data:", font=("Inter", 12, "bold")).pack(pady=(20, 5))
        cal = DateEntry(modal_dt, width=12, background=COR_NAVBAR, foreground='white', borderwidth=2, locale='pt_BR')
        cal.pack(pady=5)

        ctk.CTkLabel(modal_dt, text="Selecione o Horário:", font=("Inter", 12, "bold")).pack(pady=(20, 5))
        horarios = [f"{h:02d}:00" for h in range(8, 19)] + [f"{h:02d}:30" for h in range(8, 19)]
        horarios.sort()
        combo_hora = ctk.CTkOptionMenu(modal_dt, values=horarios, fg_color=COR_CARD, text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        combo_hora.pack(pady=5)

        def confirmar():
            data_str = cal.get_date().strftime("%d/%m/%Y")
            hora_str = combo_hora.get()
            self.controller.finalizar_venda_logica(servico, "servico", cliente, f"{data_str} às {hora_str}")
            modal_dt.destroy()

        ctk.CTkButton(modal_dt, text="Confirmar Agendamento", fg_color=COR_SUCESSO, font=("Inter", 14, "bold"), command=confirmar, height=45).pack(pady=30)

    def desenhar_tela_estoque_visualizacao(self):
        self.limpar_tela()
        
        topo_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        topo_frame.pack(fill="x", pady=20, padx=50)

        ctk.CTkLabel(topo_frame, text="📦 Inventário de Produtos", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(side="left")
        
        if self.controller.is_admin:
            ctk.CTkButton(topo_frame, text="+ Novo Produto", fg_color=COR_BOTAO_ACCENT, text_color="#000", font=("Inter", 14, "bold"), 
                          command=lambda: self.abrir_modal_produto()).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA, height=450)
        scroll.pack(fill="x", padx=50)
        
        # Cabeçalho da tabela
        h_frame = ctk.CTkFrame(scroll, fg_color=COR_NAVBAR, corner_radius=8, height=40)
        h_frame.pack(fill="x", pady=(0, 10), padx=5)
        h_frame.pack_propagate(False)
        ctk.CTkLabel(h_frame, text="Cód", width=50, text_color=COR_TEXTO_NAV, font=("Inter", 13, "bold"), anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="Nome", width=180, text_color=COR_TEXTO_NAV, font=("Inter", 13, "bold"), anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="Preço", width=80, text_color=COR_TEXTO_NAV, font=("Inter", 13, "bold"), anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="Estoque", width=80, text_color=COR_TEXTO_NAV, font=("Inter", 13, "bold"), anchor="w").pack(side="left", padx=10)
        if self.controller.is_admin:
            ctk.CTkLabel(h_frame, text="Ações", width=120, text_color=COR_TEXTO_NAV, font=("Inter", 13, "bold"), anchor="center").pack(side="right", padx=10)

        for p_row in self.controller.produtos:
            # p_row: (0:id, 1:codigo, 2:nome, 3:descricao, 4:preco, 5:estoque)
            p_id = p_row[0]
            p_codigo = str(p_row[1] or "")
            p_nome = str(p_row[2])
            p_preco = f"R$ {p_row[4]:.2f}"
            p_estoque = p_row[5]

            f = ctk.CTkFrame(scroll, fg_color="transparent", border_width=0, height=40)
            f.pack(fill="x", pady=2, padx=5)
            f.pack_propagate(False)
            
            ctk.CTkLabel(f, text=str(p_codigo), width=50, anchor="w", font=("Inter", 13), text_color=COR_INPUT_TEXTO).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=str(p_nome), width=180, anchor="w", font=("Inter", 13), text_color=COR_INPUT_TEXTO).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=str(p_preco), width=80, anchor="w", font=("Inter", 13), text_color=COR_INPUT_TEXTO).pack(side="left", padx=10)
            
            cor_q = COR_SUCESSO if p_estoque > 10 else COR_PERIGO
            ctk.CTkLabel(f, text=f"{p_estoque} un.", text_color=cor_q, font=("Inter", 13, "bold"), width=80, anchor="w").pack(side="left", padx=10)
            
            if self.controller.is_admin:
                acoes_frame = ctk.CTkFrame(f, fg_color="transparent", width=120)
                acoes_frame.pack(side="right", padx=10)
                
                # Delete
                ctk.CTkButton(acoes_frame, text="Deletar", width=30, height=30, fg_color=COR_PERIGO, 
                              command=lambda id_p=p_id: self.controller.excluir_produto(id_p)).pack(side="right", padx=2)
                # Editar
                ctk.CTkButton(acoes_frame, text="Editar", width=30, height=30, fg_color=COR_NAVBAR, 
                              command=lambda p=p_row: self.abrir_modal_produto(p)).pack(side="right", padx=2)
                # Adicionar estoque rápido
                ctk.CTkButton(acoes_frame, text="+", width=30, height=30, fg_color=COR_SUCESSO, 
                              command=lambda id_p=p_id: self.controller.alterar_estoque(id_p, 1)).pack(side="right", padx=2)
                # Remover estoque rápido
                ctk.CTkButton(acoes_frame, text="-", width=30, height=30, fg_color=COR_BOTAO_VOLTAR, 
                              command=lambda id_p=p_id: self.controller.alterar_estoque(id_p, -1)).pack(side="right", padx=2)

        ctk.CTkButton(self.content_area, text="Voltar", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR, corner_radius=20).pack(pady=25)

    def abrir_modal_produto(self, produto_dados=None):
        # produto_dados = (id, codigo, nome, descricao, preco, estoque)
        modal = ctk.CTkToplevel(self)
        modal.geometry("500x650")
        titulo = "Novo Produto" if not produto_dados else f"Editar: {produto_dados[2]}"
        modal.title(titulo)
        modal.configure(fg_color=COR_FUNDO_EXTERNO)
        modal.attributes("-topmost", True)
        modal.grab_set()

        ctk.CTkLabel(modal, text=titulo, font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        
        container = ctk.CTkFrame(modal, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        ent_codigo = self.criar_input(container, "Código (ex: PRD-001)")
        ent_nome = self.criar_input(container, "Nome do Produto *")
        ent_descricao = self.criar_input(container, "Descrição")
        ent_preco = self.criar_input(container, "Preço Unitário (R$) *")
        ent_estoque = self.criar_input(container, "Estoque Atual *")

        id_atual = None
        if produto_dados:
            id_atual = produto_dados[0]
            ent_codigo.insert(0, str(produto_dados[1] or ""))
            ent_nome.insert(0, str(produto_dados[2]))
            ent_descricao.insert(0, str(produto_dados[3] or ""))
            ent_preco.insert(0, str(produto_dados[4]))
            ent_estoque.insert(0, str(produto_dados[5]))
        else:
            ent_estoque.insert(0, "0")

        def salvar():
            cod = ent_codigo.get()
            nom = ent_nome.get()
            des = ent_descricao.get()
            pre = ent_preco.get()
            est = ent_estoque.get()
            
            sucesso = self.controller.salvar_produto(id_atual, cod, nom, des, pre, est)
            if sucesso:
                modal.destroy()

        ctk.CTkButton(modal, text="Salvar Produto", fg_color=COR_SUCESSO, font=("Inter", 14, "bold"), height=45, command=salvar).pack(pady=(0, 20))

    def desenhar_tela_funcionarios(self):
        self.limpar_tela()
        ctk.CTkLabel(self.content_area, text="👥 Nossa Equipe Petz", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        scroll = ctk.CTkScrollableFrame(self.content_area, width=600, height=400, fg_color=COR_CARD, border_width=1, border_color=COR_BORDA)
        scroll.pack()
        for func in self.controller.funcionarios:
            f = ctk.CTkFrame(scroll, fg_color="#F9F9F9", corner_radius=10)
            f.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(f, text=f"   {func}", font=("Inter", 14), text_color=COR_INPUT_TEXTO).pack(side="left", pady=15)
            if self.controller.is_admin:
                ctk.CTkButton(f, text="Demitir", fg_color=COR_PERIGO, width=80, height=30, command=lambda x=func: self.controller.demitir_funcionario(x)).pack(side="right", padx=10)
        ctk.CTkButton(self.content_area, text="Voltar", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR).pack(pady=20)

    def desenhar_tela_vendas(self):
        self.limpar_tela()
        ctk.CTkLabel(self.content_area, text="📊 Desempenho Mensal", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        cont = ctk.CTkScrollableFrame(self.content_area, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        cont.pack(fill="both", expand=True, padx=50)
        for titulo, dados, cor in [("Produtos", self.controller.vendas_produtos, COR_BOTAO_ACCENT), ("Serviços", self.controller.vendas_servicos, COR_NAVBAR)]:
            ctk.CTkLabel(cont, text=titulo, font=("Inter", 18, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=10, anchor="w", padx=20)
            total = sum(dados.values())
            for item, qtd in dados.items():
                p = (qtd / total * 100) if total > 0 else 0
                f = ctk.CTkFrame(cont, fg_color="transparent"); f.pack(fill="x", padx=20)
                ctk.CTkLabel(f, text=f"{item}", width=150, anchor="w", text_color=COR_INPUT_TEXTO).pack(side="left")
                bg = ctk.CTkFrame(f, fg_color="#EEE", height=12, width=300, corner_radius=6); bg.pack(side="left", padx=10)
                ctk.CTkFrame(bg, fg_color=cor, height=12, width=(p * 3), corner_radius=6).place(x=0, y=0)
                ctk.CTkLabel(f, text=f"{p:.1f}%", text_color=COR_INPUT_TEXTO).pack(side="left")
        ctk.CTkButton(self.content_area, text="Voltar", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR).pack(pady=10)

    def desenhar_tela_agenda(self):
        self.limpar_tela()
        ctk.CTkLabel(self.content_area, text="📅 Agenda Próximos Pets", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        scroll = ctk.CTkScrollableFrame(self.content_area, width=850, height=450, fg_color="transparent")
        scroll.pack()
        if not self.controller.agendamentos:
            ctk.CTkLabel(scroll, text="Tudo limpo por aqui!", text_color="gray", font=("Inter", 16)).pack(pady=50)
        for a in self.controller.agendamentos:
            f = ctk.CTkFrame(scroll, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
            f.pack(fill="x", pady=8, padx=20)
            ctk.CTkLabel(f, text="🐕", font=("Inter", 25)).pack(side="left", padx=(20,10), pady=15)
            info = ctk.CTkFrame(f, fg_color="transparent")
            info.pack(side="left", fill="y")
            ctk.CTkLabel(info, text=a['pet'], font=("Inter", 16, "bold"), text_color=COR_NAVBAR).pack(anchor="w", pady=(10,0))
            ctk.CTkLabel(info, text=f"Dono: {a['humano']}", font=("Inter", 12), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(f, text=a['servico'], font=("Inter", 12, "bold"), fg_color=COR_BOTAO_ACCENT, text_color="#000", corner_radius=10, width=180, height=35).pack(side="right", padx=30)
        ctk.CTkButton(self.content_area, text="Voltar ao Início", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR, height=40, corner_radius=20).pack(pady=20)
