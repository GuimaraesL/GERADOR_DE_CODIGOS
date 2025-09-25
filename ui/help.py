"""
Módulo de ajuda e integração com repositório GitHub.
Mantém a GUI principal limpa, expondo utilitários para:
- Janela de ajuda (Toplevel)
- Ícone/link do GitHub (com controle de tamanho)
"""

import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import webbrowser
from pathlib import Path

import ttkbootstrap as ttk

# Pillow é opcional: se existir, usamos para redimensionar com qualidade
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

REPO_URL = "https://github.com/GuimaraesL/GERADOR_DE_CODIGOS"
TARGET_SIZE = (16, 16)  # largura, altura desejadas do ícone


def _open_repo(url: str = REPO_URL):
    webbrowser.open(url)


def show_help(parent: tk.Misc, repo_url: str = REPO_URL):
    """Exibe a janela com guia de ajuda básico e link para o repositório."""
    win = tk.Toplevel(parent)
    win.title("Guia de ajuda")
    win.geometry("640x540")
    win.transient(parent)
    win.grab_set()

    frame = ttk.Frame(win, padding=10)
    frame.pack(fill=tk.BOTH, expand=tk.YES)

    titulo = ttk.Label(frame, text="Guia de ajuda — Gerador de Códigos", font=("Segoe UI", 12, "bold"))
    titulo.pack(anchor=tk.W, pady=(0, 8))

    texto = (
        "O que este app faz:\n"
        "- Lê uma base de códigos no Excel, identifica o próximo número disponível por sigla\n"
        "  (preenchendo lacunas) e escreve o resultado em uma nova aba 'RESULTADO' no arquivo de siglas.\n\n"
        "Como usar (passo a passo):\n"
        "1) Clique em 'Selecionar base' e escolha o Excel com os códigos existentes (aba padrão 'aba1').\n"
        "2) Clique em 'Selecionar entrada' e escolha o Excel com as siglas (aba padrão 'SIGLAS', coluna 'A').\n"
        "3) (Opcional) Marque 'Gerar códigos com 3 dígitos' para sufixos como 001 (senão usa 0001).\n"
        "4) Clique em 'Processar'. Uma nova aba 'RESULTADO' (ou RESULTADO1, ...) será criada no arquivo de siglas.\n\n"
        "Dicas:\n"
        "- Se a aba/coluna padrão não existir, o app perguntará o nome correto.\n"
        "- Feche o arquivo de siglas antes de processar (para permitir escrita).\n"
        "- Aceita formatos de código ABC0001 (4 dígitos) ou ABC001 (3 dígitos).\n\n"
        "Mais detalhes, código-fonte e issues:\n"
    )

    txt = scrolledtext.ScrolledText(frame, wrap="word", height=20)
    txt.insert("1.0", texto)
    txt.configure(state="disabled")
    txt.pack(fill=tk.BOTH, expand=tk.YES)

    # Link para o repositório (compatível com qualquer ttkbootstrap)
    link = tk.Label(frame, text="Abrir repositório no GitHub", fg="blue", cursor="hand2", font=("Segoe UI", 9))
    link.pack(anchor=tk.W, pady=(8, 0))
    link.bind("<Button-1>", lambda e: _open_repo(repo_url))


def create_github_link(parent: tk.Misc, repo_url: str = REPO_URL) -> tk.Widget:
    """
    Cria um botão/label com ícone do GitHub (se disponível) que abre o repositório.
    - Tenta carregar assets/github_16.png
    - Se não encontrar, usa fallback '🐙 GitHub' como label azul clicável.
    - Garante que a imagem exibida tenha até 16x16 px mesmo em DPI alto.
    Retorna o widget criado (para o chamador posicionar).
    """
    icon = _load_github_icon_scaled()
    if icon is not None:
        btn = ttk.Button(
            parent,
            text=" GitHub",
            image=icon,
            compound="left",
            command=lambda: _open_repo(repo_url)
        )
        btn.image = icon  # evitar GC
        btn.configure(cursor="hand2")
        return btn
    else:
        # Fallback texto/emoji estilo link (tk.Label)
        lbl = tk.Label(parent, text="🐙 GitHub", fg="blue", cursor="hand2", font=("Segoe UI", 9))
        lbl.bind("<Button-1>", lambda e: _open_repo(repo_url))
        return lbl


def _load_github_icon_scaled() -> PhotoImage | None:
    """Carrega o ícone e força tamanho alvo (16x16). Usa Pillow se disponível; senão, PhotoImage + subsample."""
    try:
        base_dir = Path(__file__).resolve().parent.parent  # .../ui -> raiz do projeto
        icon_path = base_dir / "assets" / "github_16.png"
        if not icon_path.exists():
            return None

        if PIL_AVAILABLE:
            img = Image.open(icon_path).convert("RGBA")
            if img.size != TARGET_SIZE:
                img = img.resize(TARGET_SIZE, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            # Sem Pillow: usa PhotoImage e, se maior, reduz com subsample (inteiro)
            ph = PhotoImage(file=str(icon_path))
            w, h = ph.width(), ph.height()
            max_w, max_h = TARGET_SIZE
            if w > max_w or h > max_h:
                fx = max(1, w // max_w)
                fy = max(1, h // max_h)
                ph = ph.subsample(fx, fy)
            return ph
    except Exception:
        return None