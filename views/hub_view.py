import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry 
from model.pet import PetModel
from model.cliente import ClienteModel

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
        ctk.CTkButton(self.nav_btns, text="🛒 Loja / Serviços", command=self.controller.tela_registros, **opts).pack(side="left", padx=5)
        ctk.CTkButton(self.nav_btns, text="💰 Caixa PDV", command=self.controller.tela_registro_venda, fg_color=COR_SUCESSO, text_color="#FFF", hover_color="#218838", corner_radius=20, width=110, font=("Inter", 13, "bold")).pack(side="left", padx=5)

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
        
        menu = [("AGENDA", "📅", self.controller.tela_agenda), ("CLIENTES", "👥", self.controller.tela_cadastro), ("ESTOQUE", "📦", self.controller.tela_estoque_visualizacao), ("EQUIPE", "👥", self.controller.tela_funcionarios), ("RELATÓRIOS", "📊", self.controller.tela_vendas)]
        
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

    def desenhar_tela_cadastro(self):
        self.limpar_tela()
        self.controller.current_screen = "cadastro"
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 20))
        ctk.CTkLabel(header_frame, text="👥 Gestão de Clientes & Pets", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(side="left", padx=20)
        ctk.CTkButton(header_frame, text="+ Novo Cliente", fg_color=COR_SUCESSO, font=("Inter", 14, "bold"), width=180, height=40, corner_radius=10, command=self.controller.abrir_modal_cadastro).pack(side="right", padx=20)
        scroll = ctk.CTkScrollableFrame(self.content_area, width=1000, height=500, fg_color=COR_CARD, border_width=1, border_color=COR_BORDA, corner_radius=15)
        scroll.pack(padx=20, fill="both", expand=True)
        if not self.controller.clientes:
            ctk.CTkLabel(scroll, text="Nenhum cliente cadastrado ainda.", text_color="gray", font=("Inter", 16)).pack(pady=50)
        for i, cliente_row in enumerate(self.controller.clientes):
            # cliente_row format: (id, nome, cpf, telefone, email, endereco, admin)
            c_id = cliente_row[0]
            c_nome = cliente_row[1]
            c_cpf = cliente_row[2]
            c_telefone = cliente_row[3]
            c_email = cliente_row[4]
            c_endereco = cliente_row[5]

            # Parse cliente as dict for compatibility with modal methods
            cliente = {
                'id': c_id, 'humano': c_nome, 'cpf': c_cpf, 
                'telefone': c_telefone, 'email': c_email, 'endereco': c_endereco
            }
            
            # Fetch pets
            pets_db = PetModel.listar_por_cliente(c_id)
            pets = [{'id': p[0], 'nome': p[2], 'especie': p[3], 'raca': p[4], 'idade': p[5], 'porte': p[6], 'cuidados_especiais': p[7]} for p in pets_db]
            cliente['pets'] = pets

            f = ctk.CTkFrame(scroll, fg_color="#F9F9F9", corner_radius=12, border_width=1, border_color="#EEE")
            f.pack(fill="x", pady=5, padx=10)
            info_frame = ctk.CTkFrame(f, fg_color="transparent")
            info_frame.pack(side="left", padx=20, pady=10)
            ctk.CTkLabel(info_frame, text=f"👤 {c_nome}", font=("Inter", 15, "bold"), text_color=COR_NAVBAR).pack(anchor="w")
            
            pets_str = ", ".join([p.get('nome', '') for p in pets])
            ctk.CTkLabel(info_frame, text=f"🐾 Pets: {pets_str}", font=("Inter", 12), text_color=COR_TEXTO_PADRAO).pack(anchor="w")

            btn_area = ctk.CTkFrame(f, fg_color="transparent")
            btn_area.pack(side="right", padx=15)
            ctk.CTkButton(btn_area, text="🐾 Pets", width=65, height=30, fg_color=COR_ACCENT, text_color="#000", font=("Inter", 11, "bold"), command=lambda c=cliente: self.controller.tela_pets_cliente(c)).pack(side="left", padx=5)
            ctk.CTkButton(btn_area, text="Editar", width=65, height=30, fg_color=COR_NAVBAR, command=lambda c=cliente: self.editar_cliente_modal(c)).pack(side="left", padx=5)
            ctk.CTkButton(btn_area, text="Excluir", width=65, height=30, fg_color=COR_PERIGO, command=lambda id_c=c_id: self.controller.excluir_cliente_logica(id_c)).pack(side="left", padx=5)
        ctk.CTkButton(self.content_area, text="Voltar ao Início", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR, height=40, corner_radius=20).pack(pady=20)

    def desenhar_tela_pets_cliente(self, cliente):
        self.limpar_tela()
        self.controller.current_screen = "pets_cliente"
        
        topo_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        topo_frame.pack(fill="x", pady=(10, 20), padx=20)
        
        titulo_texto = f"🐾 Pets de {cliente.get('humano', 'Cliente')}"
        ctk.CTkLabel(topo_frame, text=titulo_texto, font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(side="left")
        ctk.CTkButton(topo_frame, text="+ Novo Pet", fg_color=COR_SUCESSO, font=("Inter", 14, "bold"), width=150, height=40, corner_radius=10, 
                      command=lambda: self.modal_pet_adicional(cliente)).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.content_area, width=1000, height=500, fg_color=COR_CARD, border_width=1, border_color=COR_BORDA, corner_radius=15)
        scroll.pack(padx=20, fill="both", expand=True)

        pets = cliente.get('pets', [])
        
        if not pets:
            ctk.CTkLabel(scroll, text="Nenhum pet cadastrado para este cliente.", text_color="gray", font=("Inter", 16)).pack(pady=50)
        
        for i, pet in enumerate(pets):
            f = ctk.CTkFrame(scroll, fg_color="#F9F9F9", corner_radius=12, border_width=1, border_color="#EEE")
            f.pack(fill="x", pady=5, padx=10)
            
            info_frame = ctk.CTkFrame(f, fg_color="transparent")
            info_frame.pack(side="left", padx=20, pady=10)
            
            ctk.CTkLabel(info_frame, text=f"🐾 {pet.get('nome', 'Sem Nome')}", font=("Inter", 15, "bold"), text_color=COR_NAVBAR).pack(anchor="w")
            
            detalhes = f"Espécie: {pet.get('especie', '-')} | Raça: {pet.get('raca', '-')} | Idade: {pet.get('idade', '-')}"
            ctk.CTkLabel(info_frame, text=detalhes, font=("Inter", 12), text_color=COR_TEXTO_PADRAO).pack(anchor="w")
            
            btn_area = ctk.CTkFrame(f, fg_color="transparent")
            btn_area.pack(side="right", padx=15)
            
            ctk.CTkButton(btn_area, text="Editar", width=65, height=30, fg_color=COR_NAVBAR, 
                          command=lambda c=cliente, p=pet: self.modal_pet_adicional(c, p)).pack(side="left", padx=5)
            ctk.CTkButton(btn_area, text="Excluir", width=65, height=30, fg_color=COR_PERIGO, 
                          command=lambda c=cliente, p=pet: self.controller.excluir_pet_logica(c, p['id'])).pack(side="left", padx=5)

        ctk.CTkButton(self.content_area, text="Voltar", command=self.controller.tela_cadastro, fg_color=COR_BOTAO_VOLTAR, height=40, corner_radius=20).pack(pady=20)


    def modal_pet_adicional(self, cliente, pet_editado=None):
        modal = ctk.CTkToplevel(self)
        modal.geometry("400x650")
        
        is_edit = pet_editado is not None
        titulo = f"Editar Pet: {pet_editado['nome']}" if is_edit else f"Novo Pet para {cliente.get('humano', '')}"
        
        modal.title(titulo)
        modal.attributes("-topmost", True)
        modal.grab_set()
        ctk.CTkLabel(modal, text=f"🐾 {titulo}", font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        
        ent_pet_nome = self.criar_input(modal, "Nome do Pet")
        
        def on_especie_change(escolha):
            if escolha == "Outro": ent_custom.pack(fill="x", pady=5, padx=10)
            else: ent_custom.pack_forget()
            
        ent_especie = ctk.CTkOptionMenu(modal, values=["Cão", "Gato", "Pássaro", "Outro"], command=on_especie_change, fg_color="#F0F0F0", text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        ent_especie.pack(fill="x", pady=5, padx=10)
        ent_custom = ctk.CTkEntry(modal, placeholder_text="Qual espécie?", fg_color=COR_INPUT_BG, text_color=COR_INPUT_TEXTO)
        
        ent_raca = self.criar_input(modal, "Raça")
        ent_idade = self.criar_input(modal, "Idade")
        
        ent_porte = ctk.CTkOptionMenu(modal, values=["pequeno", "médio", "grande"], fg_color="#F0F0F0", text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        ent_porte.pack(fill="x", pady=5, padx=10)
        ent_cuidados = self.criar_input(modal, "Cuidados Especiais")
        
        if is_edit:
            pet_atual = pet_editado
            ent_pet_nome.insert(0, pet_atual.get('nome', ''))
            
            esp_atual = pet_atual.get('especie', 'Cão')
            if esp_atual in ["Cão", "Gato", "Pássaro"]:
                ent_especie.set(esp_atual)
            else:
                ent_especie.set("Outro")
                on_especie_change("Outro")
                ent_custom.insert(0, esp_atual)
                
            ent_raca.insert(0, pet_atual.get('raca', ''))
            ent_idade.insert(0, pet_atual.get('idade', ''))
            
            porte_atual = pet_atual.get('porte', 'médio')
            if porte_atual in ["pequeno", "médio", "grande"]:
                ent_porte.set(porte_atual)
            else:
                ent_porte.set("médio")
            ent_cuidados.insert(0, pet_atual.get('cuidados_especiais', ''))

        def salvar():
            if not ent_pet_nome.get(): 
                messagebox.showwarning("Atenção", "O nome do pet é obrigatório!")
                return
            esp = ent_custom.get() if ent_especie.get() == "Outro" else ent_especie.get()
            
            if 'pets' not in cliente: cliente['pets'] = []
            
            dados_pet = {"nome": ent_pet_nome.get(), "especie": esp, "raca": ent_raca.get(), "idade": ent_idade.get()}
            
            if is_edit:
                PetModel.atualizar(pet_editado['id'], ent_pet_nome.get(), esp, ent_raca.get(), ent_idade.get(), ent_porte.get(), ent_cuidados.get())
                msg = f"{ent_pet_nome.get()} atualizado!"
            else:
                PetModel.inserir(cliente['id'], ent_pet_nome.get(), esp, ent_raca.get(), ent_idade.get(), ent_porte.get(), ent_cuidados.get())
                msg = f"{ent_pet_nome.get()} adicionado à família!"
                
            modal.destroy()
            
            # Re-fetch pets to update the cliente dict
            pets_db = PetModel.listar_por_cliente(cliente['id'])
            cliente['pets'] = [{'id': p[0], 'nome': p[2], 'especie': p[3], 'raca': p[4], 'idade': p[5], 'porte': p[6], 'cuidados_especiais': p[7]} for p in pets_db]
            
            self.controller.tela_pets_cliente(cliente)
            messagebox.showinfo("Sucesso", msg)
            
        ctk.CTkButton(modal, text="Salvar Pet", fg_color=COR_SUCESSO, command=salvar, height=45).pack(pady=30)

    def editar_cliente_modal(self, cliente):
        modal = ctk.CTkToplevel(self)
        modal.geometry("450x600")
        modal.title("Editar Cliente")
        modal.attributes("-topmost", True)
        modal.grab_set()
        ctk.CTkLabel(modal, text="✏️ Editar Informações", font=("Inter", 20, "bold"), text_color=COR_NAVBAR).pack(pady=20)
        ent_nome = self.criar_input(modal, "Nome do Humano"); ent_nome.insert(0, cliente.get('humano', ""))
        ent_cpf = self.criar_input(modal, "CPF"); ent_cpf.insert(0, cliente.get('cpf', ""))
        ent_tel = self.criar_input(modal, "Telefone"); ent_tel.insert(0, cliente.get('telefone', ""))
        ent_email = self.criar_input(modal, "E-mail"); ent_email.insert(0, cliente.get('email', ""))
        ent_end = self.criar_input(modal, "Endereço"); ent_end.insert(0, cliente.get('endereco', ""))
        def salvar_edicao():
            if ClienteModel.atualizar(cliente['id'], ent_nome.get(), ent_cpf.get(), ent_tel.get(), ent_email.get(), ent_end.get()):
                modal.destroy()
                self.controller.tela_cadastro()
                messagebox.showinfo("Sucesso", "Registro atualizado!")
            else:
                messagebox.showerror("Erro", "Erro ao atualizar registro.")
        ctk.CTkButton(modal, text="Salvar Alterações", fg_color=COR_SUCESSO, command=salvar_edicao, height=45).pack(pady=30, padx=20, fill="x")

    def abrir_modal_cadastro(self, item_para_venda=None, tipo_venda=None):
        modal = ctk.CTkToplevel(self)
        modal.geometry("600x700") 
        modal.title("Novo Cadastro")
        modal.configure(fg_color=COR_FUNDO_EXTERNO)
        modal.attributes("-topmost", True); modal.grab_set()
        tabview = ctk.CTkTabview(modal, fg_color=COR_CARD, border_width=1, border_color=COR_BORDA, corner_radius=15)
        tabview.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        tab_cliente = tabview.add("👤 Cadastro Cliente")
        tab_pet = tabview.add("🐾 Cadastro Pet")
        
        ent_nome = self.criar_input(tab_cliente, "Nome Completo")
        ent_cpf = self.criar_input(tab_cliente, "CPF")
        ent_tel = self.criar_input(tab_cliente, "Telefone")
        ent_email = self.criar_input(tab_cliente, "E-mail")
        ent_end = self.criar_input(tab_cliente, "Endereço")
        
        ent_pet_nome = self.criar_input(tab_pet, "Nome do Pet")
        ent_especie = ctk.CTkOptionMenu(tab_pet, values=["Cão", "Gato", "Pássaro", "Outro"], fg_color="#F0F0F0", text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        ent_especie.pack(fill="x", pady=5, padx=10)
        ent_raca = self.criar_input(tab_pet, "Raça")
        ent_idade = self.criar_input(tab_pet, "Idade (ex: 2 anos)")

        ent_porte = ctk.CTkOptionMenu(tab_pet, values=["pequeno", "médio", "grande"], fg_color="#F0F0F0", text_color=COR_TEXTO_TITULO, button_color=COR_NAVBAR)
        ent_porte.pack(fill="x", pady=5, padx=10)
        ent_cuidados = self.criar_input(tab_pet, "Cuidados Especiais")

        def salvar():
            if not ent_nome.get():
                messagebox.showwarning("Atenção", "Preencha o Nome do Cliente!"); return
            # Check if user tried to fill pet data without a name
            pet_nome_val = ent_pet_nome.get().strip()
            pet_raca_val = ent_raca.get().strip()
            pet_idade_val = ent_idade.get().strip()
            pet_cuida_val = ent_cuidados.get().strip()
            
            tem_dado_pet = bool(pet_raca_val or pet_idade_val or pet_cuida_val)
            
            if tem_dado_pet and not pet_nome_val:
                messagebox.showwarning("Atenção", "Você começou a preencher os dados do Pet. O Nome do Pet é obrigatório!")
                return
                
            dados = {
                "humano": ent_nome.get(), 
                "cpf": ent_cpf.get(), 
                "telefone": ent_tel.get(),
                "email": ent_email.get(),
                "endereco": ent_end.get(), 
                "pets": []
            }

            if pet_nome_val:
                dados["pets"].append({
                    "nome": pet_nome_val, 
                    "especie": ent_especie.get(),
                    "raca": pet_raca_val,
                    "idade": pet_idade_val,
                    "porte": ent_porte.get(),
                    "cuidados_especiais": pet_cuida_val
                })
            
            id_novo = self.controller.salvar_cliente_com_pet(dados)
            if id_novo:
                pass # success
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar!")
                return
                
            modal.destroy()
            messagebox.showinfo("Petz", "Cadastrado!")
            
            # Re-fetch the updated format for the rest of checkout flow
            if item_para_venda:
                # Mock cliente to fit the current checkout expectations
                cliente_mock = {
                    'id': id_novo, 'humano': dados['humano'], 'cpf': dados['cpf'],
                    'telefone': dados['telefone'], 'endereco': dados['endereco'],
                    'pets': dados['pets']
                }
                
            if hasattr(self.controller, "current_screen") and self.controller.current_screen == "cadastro": self.controller.tela_cadastro()
            if item_para_venda: 
                if tipo_venda == "servico":
                    self.abrir_modal_data_hora(item_para_venda, cliente_mock)
                else:
                    self.controller.finalizar_venda_logica(item_para_venda, tipo_venda, cliente=cliente_mock)
        
        ctk.CTkButton(modal, text="Finalizar Cadastro", fg_color=COR_BOTAO_ACCENT, text_color="#000", font=("Inter", 14, "bold"), height=50, command=salvar).pack(pady=20, padx=20, fill="x")

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
            for c_row in self.controller.clientes:
                # c_row: (id, nome, cpf, telefone, email, endereco, admin)
                c_id, c_nome = c_row[0], c_row[1]
                if termo in c_nome.lower():
                    f_res = ctk.CTkFrame(lista_busca, fg_color="#F9F9F9", height=40)
                    f_res.pack(fill="x", pady=2)
                    
                    pets_db = PetModel.listar_por_cliente(c_id)
                    pets_str = ", ".join(p[2] for p in pets_db)
                    
                    # Create mock dict for check/out flow
                    c_dict = {'id': c_id, 'humano': c_nome, 'pets': [{'nome': p[2]} for p in pets_db]}
                    
                    ctk.CTkLabel(f_res, text=f"{c_nome} ({pets_str})", text_color=COR_TEXTO_TITULO, font=("Inter", 12)).pack(side="left", padx=10)
                    ctk.CTkButton(f_res, text="Selecionar", width=80, height=24, fg_color=COR_SUCESSO, 
                                  command=lambda cl=c_dict: [pop.destroy(), self.abrir_modal_data_hora(item, cl) if tipo == "servico" else self.controller.finalizar_venda_logica(item, tipo, cl)]).pack(side="right", padx=5)

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
        pets_str = ", ".join(p.get("nome", "") for p in cliente.get("pets", [])) if "pets" in cliente else cliente.get("pet", "")
        ctk.CTkLabel(modal_dt, text=f"Cliente: {cliente.get('humano', '')} & {pets_str}", font=("Inter", 12)).pack()

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
        # Legacy fallback — redirect to dashboard
        pass

    def desenhar_tela_dashboard(self, data):
        self.limpar_tela()
        self.controller.current_screen = "dashboard"

        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ===== HEADER =====
        ctk.CTkLabel(scroll, text="📊 Painel de Controle", font=("Inter", 26, "bold"), text_color=COR_NAVBAR).pack(anchor="w", padx=20, pady=(10, 20))

        # ===== KPI CARDS =====
        kpi_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=20, pady=(0, 20))

        vendas = data.get('vendas', {})
        clientes = data.get('clientes', {})
        estoque = data.get('estoque', {})

        kpis = [
            ("💰 Faturamento", f"R$ {vendas.get('faturamento', 0):.2f}", COR_SUCESSO),
            ("🛒 Vendas", str(vendas.get('num_vendas', 0)), COR_NAVBAR),
            ("🎫 Ticket Médio", f"R$ {vendas.get('ticket_medio', 0):.2f}", "#6f42c1"),
            ("👥 Clientes", str(clientes.get('total_clientes', 0)), COR_BOTAO_ACCENT),
            ("🐾 Pets", str(clientes.get('total_pets', 0)), "#e83e8c"),
            ("📦 Itens Estoque", str(estoque.get('total_itens', 0)), COR_NAVBAR),
        ]

        for i, (titulo, valor, cor) in enumerate(kpis):
            card = ctk.CTkFrame(kpi_frame, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
            card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            kpi_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(card, text=titulo, font=("Inter", 12), text_color="#888").pack(pady=(15, 5))
            ctk.CTkLabel(card, text=valor, font=("Inter", 22, "bold"), text_color=cor).pack(pady=(0, 15))

        # ===== SEÇÃO: ESTOQUE BAIXO =====
        produtos_baixo = estoque.get('produtos_baixo', [])
        if produtos_baixo:
            sec_est = ctk.CTkFrame(scroll, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
            sec_est.pack(fill="x", padx=20, pady=(0, 15))
            ctk.CTkLabel(sec_est, text="⚠️ Alerta de Estoque Baixo (≤ 5 unidades)", font=("Inter", 16, "bold"), text_color=COR_PERIGO).pack(anchor="w", padx=15, pady=10)
            for nome, qtd in produtos_baixo:
                f = ctk.CTkFrame(sec_est, fg_color="transparent")
                f.pack(fill="x", padx=15, pady=2)
                ctk.CTkLabel(f, text=f"• {nome}", font=("Inter", 13), text_color="#000", anchor="w").pack(side="left")
                cor_q = COR_PERIGO if qtd <= 2 else "#FF8C00"
                ctk.CTkLabel(f, text=f"{qtd} un.", font=("Inter", 13, "bold"), text_color=cor_q).pack(side="right", padx=15)

        # ===== CHARTS ROW: TOP PRODUTOS + TOP SERVIÇOS =====
        charts_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        charts_frame.pack(fill="x", padx=20, pady=(0, 15))
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)

        # -- Top Produtos --
        top_prod = data.get('top_produtos', [])
        card_tp = ctk.CTkFrame(charts_frame, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        card_tp.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_tp, text="🏆 Top 5 Produtos Vendidos", font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack(anchor="w", padx=15, pady=10)
        if not top_prod:
            ctk.CTkLabel(card_tp, text="Nenhuma venda de produto registrada.", text_color="gray").pack(pady=15)
        else:
            max_qtd = max(r[1] for r in top_prod) if top_prod else 1
            for nome, qtd in top_prod:
                f = ctk.CTkFrame(card_tp, fg_color="transparent")
                f.pack(fill="x", padx=15, pady=3)
                ctk.CTkLabel(f, text=nome, width=120, anchor="w", font=("Inter", 12), text_color="#000").pack(side="left")
                bar_w = max(int((qtd / max_qtd) * 200), 5)
                bg = ctk.CTkFrame(f, fg_color="#EEE", height=14, width=200, corner_radius=6)
                bg.pack(side="left", padx=10)
                ctk.CTkFrame(bg, fg_color=COR_BOTAO_ACCENT, height=14, width=bar_w, corner_radius=6).place(x=0, y=0)
                ctk.CTkLabel(f, text=str(int(qtd)), font=("Inter", 12, "bold"), text_color="#000").pack(side="left")
            ctk.CTkFrame(card_tp, fg_color="transparent", height=10).pack()  # spacer

        # -- Top Serviços --
        top_serv = data.get('top_servicos', [])
        card_ts = ctk.CTkFrame(charts_frame, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        card_ts.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_ts, text="✂️ Top 5 Serviços Realizados", font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack(anchor="w", padx=15, pady=10)
        if not top_serv:
            ctk.CTkLabel(card_ts, text="Nenhuma venda de serviço registrada.", text_color="gray").pack(pady=15)
        else:
            max_qtd_s = max(r[1] for r in top_serv) if top_serv else 1
            for nome, qtd in top_serv:
                f = ctk.CTkFrame(card_ts, fg_color="transparent")
                f.pack(fill="x", padx=15, pady=3)
                ctk.CTkLabel(f, text=nome, width=120, anchor="w", font=("Inter", 12), text_color="#000").pack(side="left")
                bar_w = max(int((qtd / max_qtd_s) * 200), 5)
                bg = ctk.CTkFrame(f, fg_color="#EEE", height=14, width=200, corner_radius=6)
                bg.pack(side="left", padx=10)
                ctk.CTkFrame(bg, fg_color=COR_NAVBAR, height=14, width=bar_w, corner_radius=6).place(x=0, y=0)
                ctk.CTkLabel(f, text=str(int(qtd)), font=("Inter", 12, "bold"), text_color="#000").pack(side="left")
            ctk.CTkFrame(card_ts, fg_color="transparent", height=10).pack()

        # ===== AGENDAMENTOS + VENDAS 7 DIAS =====
        bottom_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 15))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        # -- Agendamentos por Status --
        ag_data = data.get('agendamentos', {})
        card_ag = ctk.CTkFrame(bottom_frame, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        card_ag.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_ag, text="📅 Status dos Agendamentos", font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack(anchor="w", padx=15, pady=10)

        status_cores = {
            'agendado': ('#3498db', '🗓️'),
            'iniciado': ('#f39c12', '▶️'),
            'concluído': ('#2ecc71', '✅'),
            'pago': ('#27ae60', '💵'),
            'cancelado': ('#e74c3c', '❌'),
        }
        ag_grid = ctk.CTkFrame(card_ag, fg_color="transparent")
        ag_grid.pack(padx=15, pady=10)
        for i, (status, (cor, ico)) in enumerate(status_cores.items()):
            count = ag_data.get(status, 0)
            mini = ctk.CTkFrame(ag_grid, fg_color="#F5F5F5", corner_radius=10, width=100, height=70)
            mini.grid(row=0, column=i, padx=5, pady=5)
            mini.grid_propagate(False)
            ctk.CTkLabel(mini, text=f"{ico} {count}", font=("Inter", 18, "bold"), text_color=cor).place(relx=0.5, rely=0.35, anchor="center")
            ctk.CTkLabel(mini, text=status.capitalize(), font=("Inter", 10), text_color="#666").place(relx=0.5, rely=0.75, anchor="center")

        # -- Vendas últimos 7 dias --
        vendas_7 = data.get('vendas_7dias', [])
        card_v7 = ctk.CTkFrame(bottom_frame, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA)
        card_v7.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_v7, text="📈 Faturamento - Últimos 7 Dias", font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack(anchor="w", padx=15, pady=10)
        if not vendas_7:
            ctk.CTkLabel(card_v7, text="Sem vendas nos últimos 7 dias.", text_color="gray").pack(pady=15)
        else:
            max_val = max(r[1] for r in vendas_7) if vendas_7 else 1
            chart_area = ctk.CTkFrame(card_v7, fg_color="transparent", height=120)
            chart_area.pack(fill="x", padx=15, pady=10)
            for i, (dt, total) in enumerate(vendas_7):
                col = ctk.CTkFrame(chart_area, fg_color="transparent")
                col.pack(side="left", expand=True, fill="both")
                bar_h = max(int((float(total) / float(max_val)) * 80), 5)
                ctk.CTkLabel(col, text=f"R${float(total):.0f}", font=("Inter", 9), text_color="#666").pack()
                bar_container = ctk.CTkFrame(col, fg_color="transparent", height=85)
                bar_container.pack()
                bar_container.pack_propagate(False)
                bar = ctk.CTkFrame(bar_container, fg_color=COR_SUCESSO, width=30, height=bar_h, corner_radius=5)
                bar.pack(side="bottom")
                dia_str = dt.strftime("%d/%m") if hasattr(dt, 'strftime') else str(dt)
                ctk.CTkLabel(col, text=dia_str, font=("Inter", 9), text_color="#888").pack()

        # ===== BOTÃO VOLTAR =====
        ctk.CTkButton(scroll, text="Voltar ao Início", command=self.controller.mostrar_controle, fg_color=COR_BOTAO_VOLTAR, height=40, corner_radius=20).pack(pady=20)

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

    # ================= REGISTRO DE VENDA (PDV) =====================
    def desenhar_tela_registro_venda(self):
        self.limpar_tela()
        self.controller.current_screen = "venda"
        
        # Header
        top_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        top_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(top_frame, text="💰 Fechamento de Venda", font=("Inter", 24, "bold"), text_color=COR_NAVBAR).pack(side="left", padx=20)

        main_split = ctk.CTkFrame(self.content_area, fg_color="transparent")
        main_split.pack(fill="both", expand=True, padx=20)
        
        left_panel = ctk.CTkFrame(main_split, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_panel = ctk.CTkFrame(main_split, fg_color=COR_CARD, corner_radius=15, border_width=1, border_color=COR_BORDA, width=350)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # -- LEFT PANEL: Busca Cliente & Itens Disponíveis --
        
        # 1. Seleção de Cliente
        cli_frame = ctk.CTkFrame(left_panel, fg_color=COR_CARD, corner_radius=10, border_width=1, border_color=COR_BORDA)
        cli_frame.pack(fill="x", pady=(0, 10))
        
        cli_header = ctk.CTkFrame(cli_frame, fg_color="transparent")
        cli_header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(cli_header, text="1. Selecionar Cliente", font=("Inter", 16, "bold"), text_color=COR_TEXTO_TITULO).pack(side="left")
        
        b_cli = ctk.CTkEntry(cli_header, placeholder_text="Buscar cliente por nome...", width=250)
        b_cli.pack(side="left", padx=(20, 10))
        
        cliente_selecionado_lbl = ctk.CTkLabel(cli_header, text="Nenhum cliente selecionado.", text_color=COR_PERIGO, font=("Inter", 12, "bold"))
        cliente_selecionado_lbl.pack(side="right", padx=10)
        
        btn_limpar = ctk.CTkButton(cli_header, text="❌", width=25, height=25, fg_color="transparent", text_color=COR_PERIGO, hover_color="#f0f0f0")
        
        res_list = ctk.CTkScrollableFrame(cli_frame, fg_color="transparent", height=120)
        res_list.pack(fill="x", padx=10, pady=(0, 10))

        def on_cliente_search(e=None):
            for w in res_list.winfo_children(): w.destroy()
            termo = b_cli.get().lower()
            
            # Opção Visitante sempre no topo
            f_vis = ctk.CTkFrame(res_list, fg_color="#F0F0F0")
            f_vis.pack(fill="x", pady=2)
            ctk.CTkLabel(f_vis, text="🚶 Visitante (Sem Agenda/Cadastro)", text_color=COR_TEXTO_TITULO).pack(side="left", padx=5)
            ctk.CTkButton(f_vis, text="Selecionar", width=70, height=25, fg_color=COR_BOTAO_ACCENT, text_color="#000",
                          command=lambda: set_cliente({'id': 0, 'humano': 'Visitante'})).pack(side="right", padx=5)

            resultados = self.controller.clientes
            if termo:
                resultados = [c for c in self.controller.clientes if termo in c[1].lower()]
                
            for c in resultados:
                # c: (id, nome, cpf, telefone, email, endereco, admin)
                f = ctk.CTkFrame(res_list, fg_color="#F0F0F0")
                f.pack(fill="x", pady=2)
                ctk.CTkLabel(f, text=c[1], text_color=COR_TEXTO_TITULO).pack(side="left", padx=5)
                ctk.CTkButton(f, text="Selecionar", width=70, height=25, fg_color=COR_NAVBAR, 
                              command=lambda cl={'id': c[0], 'humano': c[1]}: set_cliente(cl)).pack(side="right", padx=5)
                              
        b_cli.bind("<KeyRelease>", on_cliente_search)
        on_cliente_search()  # Popular lista inicial

        # 2. Tabs: Serviços Concluídos / Produtos
        tabview = ctk.CTkTabview(left_panel, fg_color=COR_CARD, border_width=1, border_color=COR_BORDA, corner_radius=10)
        tabview.pack(fill="both", expand=True)
        tab_sv = tabview.add("Serviços à Pagar")
        tab_pr = tabview.add("Produtos Avulsos")

        def limpar_cliente():
            self.controller.carrinho_cliente = None
            self.controller.carrinho_itens = []
            cliente_selecionado_lbl.configure(text="Nenhum cliente selecionado.", text_color=COR_PERIGO)
            btn_limpar.pack_forget()
            b_cli.delete(0, 'end')
            on_cliente_search()
            for w in tab_sv.winfo_children(): w.destroy()
            atualizar_carrinho()
            
        btn_limpar.configure(command=limpar_cliente)

        def set_cliente(c_dict):
            # c_dict: {'id', 'humano'}
            self.controller.carrinho_cliente = c_dict
            self.controller.carrinho_itens = []
            cliente_selecionado_lbl.configure(text=f"Cliente: {c_dict['humano']}", text_color=COR_SUCESSO)
            btn_limpar.pack(side="right", padx=5)
            for w in res_list.winfo_children(): w.destroy()
            b_cli.delete(0, 'end')
            
            # Load Serviços não pagos
            servicos = self.controller.buscar_servicos_nao_pagos(c_dict['id'])
            for w in tab_sv.winfo_children(): w.destroy()
            if not servicos:
                ctk.CTkLabel(tab_sv, text="Não há serviços pendentes de pagamento.", text_color="gray").pack(pady=20)
            else:
                for s in servicos:
                    f = ctk.CTkFrame(tab_sv, fg_color="#F9F9F9"); f.pack(fill="x", pady=2)
                    ctk.CTkLabel(f, text=f"{s[1]} (Pet: {s[3]})", font=("Inter", 13, "bold"), text_color=COR_TEXTO_TITULO).pack(side="left", padx=10)
                    ctk.CTkLabel(f, text=f"R$ {s[2]:.2f}", font=("Inter", 13), text_color="#000").pack(side="left", padx=10)
                    ctk.CTkButton(f, text="+ Adicionar", fg_color=COR_SUCESSO, width=80, height=25,
                                  command=lambda ag_id=s[0], sn=s[1], pr=s[2]: add_item('servico', sn, pr, ag_id=ag_id)).pack(side="right", padx=10)
            
            atualizar_carrinho()

        # Popular a Tab de Produtos
        b_prod = ctk.CTkEntry(tab_pr, placeholder_text="Buscar produto...")
        b_prod.pack(fill="x", pady=5, padx=10)
        p_list = ctk.CTkScrollableFrame(tab_pr, fg_color="transparent")
        p_list.pack(fill="both", expand=True)
        
        def render_produtos(termo=""):
            for w in p_list.winfo_children(): w.destroy()
            for p in self.controller.produtos:
                if termo in p[2].lower() and p[5] > 0:
                    f = ctk.CTkFrame(p_list, fg_color="#F9F9F9"); f.pack(fill="x", pady=2)
                    ctk.CTkLabel(f, text=p[2], width=150, anchor="w", text_color=COR_TEXTO_TITULO).pack(side="left", padx=10)
                    ctk.CTkLabel(f, text=f"R$ {p[4]:.2f} (Est: {p[5]})", text_color="#000").pack(side="left", padx=10)
                    ctk.CTkButton(f, text="+ Add", fg_color=COR_SUCESSO, width=60, height=25,
                                  command=lambda id_p=p[0], nom=p[2], prc=p[4], est=p[5]: add_item('produto', nom, prc, id_p=id_p, estoque_max=est)).pack(side="right", padx=10)
        
        b_prod.bind("<KeyRelease>", lambda e: render_produtos(b_prod.get().lower()))
        render_produtos()

        # -- RIGHT PANEL: Carrinho --
        ctk.CTkLabel(right_panel, text="🛒 Subtotal", font=("Inter", 18, "bold"), text_color=COR_TEXTO_TITULO).pack(pady=15)
        cart_list = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
        cart_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        lbl_total = ctk.CTkLabel(right_panel, text="Total: R$ 0.00", font=("Inter", 22, "bold"), text_color=COR_NAVBAR)
        lbl_total.pack(pady=10)
        
        ctk.CTkButton(right_panel, text="Finalizar Venda", fg_color=COR_BOTAO_ACCENT, text_color="#000", font=("Inter", 16, "bold"), height=50, 
                      command=self.controller.fechar_venda).pack(fill="x", padx=20, pady=20)

        def add_item(tipo, nome, preco, id_p=None, ag_id=None, estoque_max=None):
            if not self.controller.carrinho_cliente:
                messagebox.showwarning("Aviso", "Selecione o Cliente primeiro.")
                return
            
            # Checar se ja ta no carrinho 
            for it in self.controller.carrinho_itens:
                if tipo == 'produto' and it['id'] == id_p:
                    if estoque_max is not None and it['qtd'] >= estoque_max:
                        messagebox.showwarning("Estoque Insuficiente", f"Você não pode adicionar mais de {estoque_max} unidades de {nome} (estoque esgotado).")
                        return
                    it['qtd'] += 1
                    atualizar_carrinho()
                    return
                elif tipo == 'servico' and it['id_agendamento'] == ag_id:
                    messagebox.showinfo("Aviso", "Serviço já adicionado.")
                    return
            
            if tipo == 'produto' and estoque_max is not None and estoque_max < 1:
                 messagebox.showwarning("Estoque Insuficiente", f"O produto {nome} está esgotado.")
                 return

            novo = {'tipo': tipo, 'id': id_p if id_p else 0, 'nome': nome, 'preco': preco, 'qtd': 1, 'id_agendamento': ag_id}
            self.controller.carrinho_itens.append(novo)
            atualizar_carrinho()

        def remover_item(idx):
            self.controller.carrinho_itens.pop(idx)
            atualizar_carrinho()

        def atualizar_carrinho():
            for w in cart_list.winfo_children(): w.destroy()
            total = 0
            for i, it in enumerate(self.controller.carrinho_itens):
                f = ctk.CTkFrame(cart_list, fg_color="#F0F0F0")
                f.pack(fill="x", pady=2)
                sub = it['preco'] * it['qtd']
                total += sub
                
                texto = f"{it['qtd']}x {it['nome']} - R${sub:.2f}"
                ctk.CTkLabel(f, text=texto, text_color=COR_TEXTO_TITULO, font=("Inter", 12)).pack(side="left", padx=5)
                ctk.CTkButton(f, text="X", width=25, height=25, fg_color=COR_PERIGO, 
                              command=lambda idx=i: remover_item(idx)).pack(side="right", padx=5)
            
            lbl_total.configure(text=f"Total: R$ {total:.2f}")

        # Se ja tiver um carrinho ativo (caso refresh da tela pos-venda), re-renderize
        if self.controller.carrinho_cliente:
            set_cliente(self.controller.carrinho_cliente)
