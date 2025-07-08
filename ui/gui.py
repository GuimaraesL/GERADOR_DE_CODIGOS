import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import json
from core.code_generator import proximo_codigo
from core.excel_processor import (
    carregar_codigos_existentes,
    extrair_siglas,
    salvar_resultado
)
from utils.helpers import letra_para_coluna
from config.texts import TEXTS

class App:
    def __init__(self, root):
        print("Classe App correta carregada de:", __file__)
        self.root = root
        self.root.title(TEXTS["app_title"])
        self.root.geometry("440x280")

        self.base_path = ""
        self.siglas_path = ""
        self.modo_tres_siglas = ttk.BooleanVar()

        container = ttk.Frame(root, padding=10)
        container.pack(fill=BOTH, expand=YES)

        ttk.Button(container, text=TEXTS["btn_select_base"], command=self.load_base, bootstyle=SUCCESS).pack(fill=X, pady=5)
        ttk.Button(container, text=TEXTS["btn_select_entrada"], command=self.load_entrada, bootstyle=PRIMARY).pack(fill=X, pady=5)
        ttk.Checkbutton(container, text="Gerar códigos com 3 dígitos", variable=self.modo_tres_siglas, bootstyle="info").pack(anchor=W, pady=5)
        ttk.Button(container, text=TEXTS["btn_processar"], command=self.processar, bootstyle=WARNING).pack(fill=X, pady=10)

        ttk.Label(container, text="Made by GuimaraesL", font=("Segoe UI", 8, "italic"), bootstyle="secondary").pack(side=BOTTOM, pady=5)

    def load_base(self):
        self.base_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.base_path:
            try:
                carregar_codigos_existentes(self.base_path)
                messagebox.showinfo("Sucesso", "Base de códigos carregada!")
            except Exception:
                aba_manual = simpledialog.askstring("Erro", "Erro ao ler a aba 'aba1'. Digite o nome correto:")
                try:
                    carregar_codigos_existentes(self.base_path, aba=aba_manual)
                    messagebox.showinfo("Sucesso", f"Base de códigos carregada da aba '{aba_manual}'!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao carregar a aba '{aba_manual}': {e}")

    def load_entrada(self):
        self.siglas_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.siglas_path:
            messagebox.showinfo("Sucesso", "Arquivo com siglas carregado!")

    def processar(self):
        if not self.base_path or not self.siglas_path:
            messagebox.showerror("Erro", "Selecione ambos os arquivos.")
            return

        aba_siglas = "SIGLAS"
        col_siglas = "A"
        aba_saida = "RESULTADO"
        col_num = letra_para_coluna(col_siglas)

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
                return

        with open("codigos.json") as f:
            df_base = pd.DataFrame(json.load(f))

        novos = []
        for sigla in df_siglas["Sigla"]:
            if pd.notna(sigla):
                novo = proximo_codigo(sigla, df_base, digitos=3 if self.modo_tres_siglas.get() else 4)
                df_base.loc[len(df_base)] = {"Codigo": novo}
                novos.append(novo)
            else:
                novos.append(None)

        df_result = pd.DataFrame({
            "Sigla": df_siglas["Sigla"],
            "Proximo_Codigo": novos
        })

        salvar_resultado(self.siglas_path, aba_saida, df_result)
        messagebox.showinfo("Sucesso", TEXTS["msg_final"])