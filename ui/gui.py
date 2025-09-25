import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
import pandas as pd
import json

from core.code_generator import proximo_codigo
from core.excel_processor import (
    carregar_codigos_existentes,
    extrair_siglas,
    salvar_resultado
)
from core.fast_code_generator import gerar_codigos_em_lote
from utils.helpers import letra_para_coluna
from config.texts import TEXTS

from ui.help import show_help  # removido create_github_link aqui (reutilizado apenas na ajuda)
from ui.theme import apply_theme, AVAILABLE_THEMES


class App:
    def __init__(self, root):
        print("Classe App correta carregada de:", __file__)
        self.root = root
        self.root.title(TEXTS["app_title"])
        self.root.minsize(560, 420)

        # ===== Estado =====
        self.base_path = ""
        self.siglas_path = ""
        self.modo_tres_siglas = ttk.BooleanVar()
        self.theme_var = tk.StringVar(value="flatly")
        self.style = apply_theme(self.theme_var.get())

        # ===== UI =====
        self._build_ui()
        self._bind_shortcuts()
        self._set_status("Pronto")

    # ---------- UI ----------
    def _build_ui(self):
        root = self.root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        # Header
        header = ttk.Frame(root, padding=(12, 12, 12, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title = ttk.Label(header, text="🔢 Gerador de Códigos", style="Title.TLabel")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(header, text="Gere automaticamente o próximo código por sigla",
                             style="Subtitle.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        theme_box = ttk.Combobox(
            header, state="readonly",
            values=AVAILABLE_THEMES, textvariable=self.theme_var, width=12
        )
        theme_box.grid(row=0, column=1, rowspan=2, sticky="e")
        theme_box.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Conteúdo
        content = ttk.Frame(root, padding=(12, 0, 12, 0))
        content.grid(row=1, column=0, sticky="nsew")
        for i in range(3):
            content.columnconfigure(i, weight=1)
        content.rowconfigure(0, weight=1)

        # Card: Arquivos
        card_files = ttk.Labelframe(content, text="Arquivos", style="Card.TLabelframe", padding=10)
        card_files.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=6)

        ttk.Button(card_files, text="📂 Selecionar base", command=self.load_base, bootstyle=SUCCESS)\
            .pack(fill=X, pady=4)
        ttk.Button(card_files, text="🧾 Selecionar entrada (siglas)", command=self.load_entrada, bootstyle=PRIMARY)\
            .pack(fill=X, pady=4)

        # Card: Opções
        card_opts = ttk.Labelframe(content, text="Opções", style="Card.TLabelframe", padding=10)
        card_opts.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        ttk.Checkbutton(
            card_opts,
            text="Gerar códigos com 3 dígitos (ex.: ABC001)",
            variable=self.modo_tres_siglas,
            bootstyle="info"
        ).pack(anchor=W, pady=4)

        # Card: Ações
        card_actions = ttk.Labelframe(content, text="Ações", style="Card.TLabelframe", padding=10)
        card_actions.grid(row=0, column=2, sticky="nsew", padx=(6, 0), pady=6)

        ttk.Button(card_actions, text="▶️ Processar", command=self.processar, bootstyle=PRIMARY)\
            .pack(fill=X, pady=4)
        ttk.Button(card_actions, text="❓ Ajuda", command=lambda: show_help(self.root), bootstyle=SUCCESS)\
            .pack(fill=X, pady=4)

        # Rodapé (status + made by centralizado) — sem ícone do GitHub
        footer = ttk.Frame(root, padding=(12, 8, 12, 12))
        footer.grid(row=2, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=1)   # central
        footer.columnconfigure(2, weight=1)   # vazio (mantém centralização)

        self.status_label = ttk.Label(footer, text="Pronto", style="Status.TLabel")
        self.status_label.grid(row=0, column=0, sticky="w")

        made_by = ttk.Label(footer, text="Made by GuimaraesL", style="Status.TLabel")
        made_by.grid(row=0, column=1, sticky="n")

        # coluna 2 propositalmente vazia (sem GitHub aqui)

    def _bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.load_base())
        self.root.bind("<Control-i>", lambda e: self.load_entrada())
        self.root.bind("<Control-p>", lambda e: self.processar())
        self.root.bind("<F1>",       lambda e: show_help(self.root))

    def _on_theme_change(self, *_):
        self.style = apply_theme(self.theme_var.get())

    def _set_status(self, msg: str):
        self.status_label.configure(text=msg)
        self.root.update_idletasks()

    # ---------- Fluxo ----------
    def load_base(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self._set_status("Carregando base...")
            self.base_path = path
            try:
                carregar_codigos_existentes(self.base_path)
                messagebox.showinfo("Sucesso", "Base de códigos carregada!")
                self._set_status("Base carregada")
            except Exception:
                aba_manual = simpledialog.askstring("Erro", "Erro ao ler a aba 'aba1'. Digite o nome correto:")
                try:
                    carregar_codigos_existentes(self.base_path, aba=aba_manual)
                    messagebox.showinfo("Sucesso", f"Base carregada da aba '{aba_manual}'!")
                    self._set_status("Base carregada")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao carregar a aba '{aba_manual}': {e}")
                    self._set_status("Erro ao carregar base")

    def load_entrada(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.siglas_path = path
            messagebox.showinfo("Sucesso", "Arquivo com siglas carregado!")
            self._set_status("Entrada carregada")

    def processar(self):
        if not self.base_path or not self.siglas_path:
            messagebox.showerror("Erro", "Selecione ambos os arquivos.")
            return

        # Padrões
        aba_siglas = "SIGLAS"
        col_siglas = "A"
        aba_saida = "RESULTADO"

        # Converte letra -> número (helpers.py)
        col_num = letra_para_coluna(col_siglas)

        self._set_status("Lendo siglas...")
        try:
            df_siglas = extrair_siglas(self.siglas_path, aba_siglas, col_num)
        except Exception:
            aba_siglas = simpledialog.askstring("Erro", "Erro ao ler a aba 'SIGLAS'. Digite o nome correto:")
            col_siglas = simpledialog.askstring("Erro", "Erro ao ler a coluna 'A'. Digite a letra correta:")
            col_num = letra_para_coluna(col_siglas)
            try:
                df_siglas = extrair_siglas(self.siglas_path, aba_siglas, col_num)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao extrair siglas: {e}")
                self._set_status("Erro ao ler siglas")
                return

        self._set_status("Processando...")
        # Carrega base (json gerado anteriormente)
        with open("codigos.json") as f:
            df_base = pd.DataFrame(json.load(f))

        # Geração em lote otimizada
        digitos = 3 if self.modo_tres_siglas.get() else 4
        siglas_lista = [s if (isinstance(s, str) or pd.isna(s)) else None for s in df_siglas["Sigla"].tolist()]
        novos = gerar_codigos_em_lote(siglas_lista, df_base, digitos=digitos)

        # Atualiza df_base conforme antes
        novos_validos = [c for c in novos if c is not None]
        if novos_validos:
            df_base = pd.concat([df_base, pd.DataFrame({"Codigo": novos_validos})], ignore_index=True)

        df_result = pd.DataFrame({
            "Sigla": df_siglas["Sigla"],
            "Proximo_Codigo": novos
        })

        salvar_resultado(self.siglas_path, aba_saida, df_result)
        self._set_status("Concluído")
        messagebox.showinfo("Sucesso", TEXTS["msg_final"])