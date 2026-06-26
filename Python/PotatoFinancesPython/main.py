import customtkinter as ctk
import database
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import os

# Configuração básica
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Potato Finances")
janela.geometry("1000x800")

lbl_saldo_valor = None
lbl_receitas_valor = None
lbl_despesas_valor = None
lbl_investimentos_valor = None

# Opções para os menus do popup
CATEGORIAS = ["Geral", "Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Salário", "Freelance", "Investimento"]
FORMAS_PAGAMENTO = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro", "Boleto", "Transferência"]

def desenhar_grafico():
    for widget in frame_grafico.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots(figsize=(8, 3.5), facecolor='#2A2D3E')
    ax.set_facecolor('#2A2D3E')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#4B5563')
        
    df = database.ler_transacoes()
    if df.empty:
        ax.text(0.5, 0.5, "Sem transações", color='white', ha='center', va='center', fontsize=12)
    else:
        df['data_transacao'] = pd.to_datetime(df['data_transacao'])
        df_chart = df[df['tipo'].isin(['Receita', 'Despesa', 'Investimento'])].copy()
        if not df_chart.empty:
            df_chart['mes_ano'] = df_chart['data_transacao'].dt.strftime('%m/%Y')
            resumo = df_chart.groupby(['mes_ano', 'tipo'])['valor'].sum().unstack().fillna(0)
            if 'Receita' in resumo.columns:
                ax.plot(resumo.index, resumo['Receita'], marker='o', color='#10B981', label='Receitas', linewidth=2)
            if 'Despesa' in resumo.columns:
                ax.plot(resumo.index, resumo['Despesa'], marker='o', color='#EF4444', label='Despesas', linewidth=2)
            if 'Investimento' in resumo.columns:
                ax.plot(resumo.index, resumo['Investimento'], marker='o', color='#8B5CF6', label='Investimentos', linewidth=2)
            ax.legend(facecolor='#2A2D3E', edgecolor='#4B5563', labelcolor='white')
            ax.set_title("Visão Anual", color='white', loc='left', pad=10)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

def deletar_item(id_transacao):
    database.deletar_transacao(id_transacao)
    atualizar_dashboard()

def abrir_transacao(modo="novo", transacao_id=None, dados=None):
    popup = ctk.CTkToplevel(janela)
    popup.title("Editar transação" if modo == "editar" else "Nova transação")
    popup.geometry("550x550")
    popup.grab_set()
    
    tipo_var = ctk.StringVar(value=dados['tipo'] if dados is not None else "Despesa")
    ctk.CTkSegmentedButton(popup, values=["Despesa", "Receita", "Investimento"], variable=tipo_var).pack(pady=(20, 10), padx=20, fill="x")
    
    ctk.CTkLabel(popup, text="Descrição").pack(anchor="w", padx=20)
    entry_descricao = ctk.CTkEntry(popup)
    entry_descricao.insert(0, dados['descricao'] if dados is not None else "")
    entry_descricao.pack(pady=(0, 10), padx=20, fill="x")
    
    ctk.CTkLabel(popup, text="Valor (R$)").pack(anchor="w", padx=20)
    entry_valor = ctk.CTkEntry(popup)
    entry_valor.insert(0, str(dados['valor']) if dados is not None else "")
    entry_valor.pack(pady=(0, 10), padx=20, fill="x")
    
    frame_linha = ctk.CTkFrame(popup, fg_color="transparent")
    frame_linha.pack(fill="x", padx=20, pady=(0, 10))
    
    ctk.CTkLabel(frame_linha, text="Data (DD/MM/AAAA)").pack(side="left")
    entry_data = ctk.CTkEntry(frame_linha, width=120)
    data_formatada = pd.to_datetime(dados['data_transacao']).strftime('%d/%m/%Y') if dados is not None else datetime.today().strftime('%d/%m/%Y')
    entry_data.insert(0, data_formatada)
    entry_data.pack(side="left", padx=(5, 0))

    ctk.CTkLabel(popup, text="Categoria").pack(anchor="w", padx=20)
    categoria_var = ctk.StringVar(value=dados['categoria'] if dados is not None else "Geral")
    ctk.CTkOptionMenu(popup, values=CATEGORIAS, variable=categoria_var).pack(pady=(0, 10), padx=20, fill="x")

    ctk.CTkLabel(popup, text="Forma de Pagamento").pack(anchor="w", padx=20)
    pagamento_var = ctk.StringVar(value=dados['forma_pagamento'] if dados is not None else "Pix")
    ctk.CTkOptionMenu(popup, values=FORMAS_PAGAMENTO, variable=pagamento_var).pack(pady=(0, 10), padx=20, fill="x")

    def salvar():
        tipo = tipo_var.get()
        descricao = entry_descricao.get()
        valor = float(entry_valor.get().replace(",", "."))
        data_mysql = datetime.strptime(entry_data.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
        categoria = categoria_var.get()
        pagamento = pagamento_var.get()
        
        if modo == "novo":
            database.inserir_transacao(tipo, descricao, valor, data_mysql, categoria, pagamento)
        else:
            database.atualizar_transacao(transacao_id, tipo, descricao, valor, data_mysql, categoria, pagamento)
            
        atualizar_dashboard()
        popup.destroy()

    ctk.CTkButton(popup, text="Salvar", fg_color="#7C3AED", command=salvar).pack(pady=10, padx=20, fill="x")

def desenhar_tabela():
    for widget in frame_lista.winfo_children(): widget.destroy()
    df = database.ler_transacoes()
    if df.empty: return
    df = df.sort_values(by='data_transacao', ascending=False)
    for _, row in df.iterrows():
        linha = ctk.CTkFrame(frame_lista, fg_color="#374151", corner_radius=5)
        linha.pack(fill="x", pady=2, padx=2)
        # Botões empacotados PRIMEIRO (side=right) para garantir visibilidade
        btn_edit = ctk.CTkButton(linha, text="✎", width=28, fg_color="#3B82F6", command=lambda r=row: abrir_transacao(modo="editar", transacao_id=r['id'], dados=r))
        btn_edit.pack(side="right", padx=(2, 5))
        btn_del = ctk.CTkButton(linha, text="X", width=28, fg_color="#EF4444", command=lambda id_t=row['id']: deletar_item(id_t))
        btn_del.pack(side="right", padx=2)
        # Labels empacotados DEPOIS — se faltar espaço, o texto trunca mas os botões permanecem
        ctk.CTkLabel(linha, text=pd.to_datetime(row['data_transacao']).strftime('%d/%m/%Y'), width=70).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=row['descricao'], width=120, anchor="w").pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkLabel(linha, text=f"R$ {row['valor']:.2f}", width=80).pack(side="left", padx=5)

def atualizar_dashboard():
    df = database.ler_transacoes()
    total_rec = df[df['tipo'] == 'Receita']['valor'].sum() if not df.empty else 0
    total_desp = df[df['tipo'] == 'Despesa']['valor'].sum() if not df.empty else 0
    total_inv = df[df['tipo'] == 'Investimento']['valor'].sum() if not df.empty else 0
    lbl_saldo_valor.configure(text=f"R$ {total_rec - total_desp - total_inv:,.2f}")
    lbl_receitas_valor.configure(text=f"R$ {total_rec:,.2f}")
    lbl_despesas_valor.configure(text=f"R$ {total_desp:,.2f}")
    lbl_investimentos_valor.configure(text=f"R$ {total_inv:,.2f}")
    desenhar_grafico()
    desenhar_tabela()

# --- LAYOUT PRINCIPAL ---
frame_topo = ctk.CTkFrame(janela, fg_color="transparent")
frame_topo.pack(pady=20, padx=20, fill="x")

# Logo + Título
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
logo_pil = Image.open(logo_path)
logo_ratio = logo_pil.width / logo_pil.height
logo_height = 80
logo_image = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(int(logo_height * logo_ratio), logo_height))
ctk.CTkLabel(frame_topo, image=logo_image, text="").pack(side="left", padx=(0, 10))
ctk.CTkLabel(frame_topo, text="Potato Finances", font=("Arial", 32, "bold")).pack(side="left")
ctk.CTkButton(frame_topo, text="+ Nova transação", fg_color="#7C3AED", command=lambda: abrir_transacao(modo="novo")).pack(side="right")

frame_cards = ctk.CTkFrame(janela, fg_color="transparent")
frame_cards.pack(pady=10, padx=20, fill="x")

def criar_card(pai, titulo, cor):
    card = ctk.CTkFrame(pai, height=100, corner_radius=15, fg_color="#2A2D3E")
    card.pack(side="left", padx=10, expand=True, fill="both")
    ctk.CTkLabel(card, text=titulo).pack(pady=10)
    lbl = ctk.CTkLabel(card, text="R$ 0,00", font=("Arial", 20, "bold"), text_color=cor)
    lbl.pack(pady=10)
    return lbl

lbl_saldo_valor = criar_card(frame_cards, "Saldo", "#10B981")
lbl_receitas_valor = criar_card(frame_cards, "Receitas", "#10B981")
lbl_despesas_valor = criar_card(frame_cards, "Despesas", "#EF4444")
lbl_investimentos_valor = criar_card(frame_cards, "Investimentos", "#8B5CF6")

area_inferior = ctk.CTkFrame(janela, fg_color="transparent")
area_inferior.pack(pady=10, padx=20, fill="both", expand=True)
frame_grafico = ctk.CTkFrame(area_inferior, corner_radius=15, fg_color="#2A2D3E")
frame_grafico.pack(side="left", fill="both", expand=True, padx=(0, 10))
frame_historico = ctk.CTkFrame(area_inferior, corner_radius=15, fg_color="#2A2D3E")
frame_historico.pack(side="right", fill="both", expand=False)
frame_lista = ctk.CTkScrollableFrame(frame_historico, fg_color="transparent", width=420)
frame_lista.pack(fill="both", expand=True, padx=5, pady=5)

atualizar_dashboard()
janela.mainloop()