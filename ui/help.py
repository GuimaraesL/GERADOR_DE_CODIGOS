"""
Módulo de ajuda e integração com repositório GitHub.
- Janela de ajuda (Toplevel) clara e persuasiva
- Ícone/link do GitHub reutilizável (com controle de tamanho 16x16)
"""

import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import webbrowser
from pathlib import Path

import ttkbootstrap as ttk

# Pillow é opcional; se existir, redimensiona melhor o ícone
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

REPO_URL = "https://github.com/GuimaraesL/GERADOR_DE_CODIGOS"
TARGET_SIZE = (16, 16)  # tamanho alvo do ícone


def _open_repo(url: str = REPO_URL):
    webbrowser.open(url)


def show_help(parent: tk.Misc, repo_url: str = REPO_URL):
    """Exibe a janela com guia de ajuda aprimorado e ícone clicável do GitHub."""
    win = tk.Toplevel(parent)
    win.title("Guia de ajuda")
    win.geometry("640x560")
    win.transient(parent)
    win.grab_set()

    frame = ttk.Frame(win, padding=10)
    frame.pack(fill=tk.BOTH, expand=tk.YES)

    # Cabeçalho da ajuda
    titulo = ttk.Label(frame, text="📘 Guia de Ajuda — Gerador de Códigos", font=("Segoe UI", 14, "bold"))
    titulo.pack(anchor=tk.W, pady=(0, 10))

    # Corpo do texto (claro e persuasivo)
    texto = (
        "O que este app faz:\n"
        "Gera automaticamente códigos sequenciais a partir de siglas, preenchendo lacunas e salvando o resultado no Excel.\n\n"

        "Como usar (passo a passo):\n"
        "1️⃣ Clique em 'Selecionar base' e escolha o Excel com os códigos existentes (aba padrão: aba1).\n"
        "2️⃣ Clique em 'Selecionar entrada' e escolha o Excel com as siglas (aba padrão: SIGLAS, coluna A).\n"
        "3️⃣ (Opcional) Marque 'Gerar códigos com 3 dígitos' para usar formato ABC001 (senão usa ABC0001).\n"
        "4️⃣ Clique em 'Processar'. O resultado será gravado em uma nova aba 'RESULTADO'.\n\n"

        "Dicas importantes:\n"
        "✔ Feche o arquivo de siglas antes de processar (para permitir escrita).\n"
        "✔ Se a aba ou coluna padrão não existir, o app perguntará o nome correto.\n"
        "✔ Aceita formatos ABC0001 (4 dígitos) ou ABC001 (3 dígitos).\n\n"

        "Mais recursos no GitHub (recomendado):\n"
        "- Documentação completa (README com exemplos e diagramas)\n"
        "- Roadmap e melhorias futuras\n"
        "- Espaço para reportar problemas (Issues)\n\n"
        "Clique no ícone do GitHub abaixo para abrir o repositório:\n"
    )

    txt = scrolledtext.ScrolledText(frame, wrap="word", height=22)
    txt.insert("1.0", texto)
    txt.configure(state="disabled")
    txt.pack(fill=tk.BOTH, expand=tk.YES)

    # CTA com ícone reaproveitado do GitHub (botão com imagem 16x16)
    cta = ttk.Frame(frame)
    cta.pack(anchor=tk.W, pady=(8, 0))

    gh_btn = create_github_link(cta, repo_url=repo_url)
    gh_btn.pack(side=tk.LEFT)

    # Opcional: legenda ao lado do ícone (não clicável)
    legenda = ttk.Label(cta, text="Abrir repositório no GitHub", font=("Segoe UI", 10))
    legenda.pack(side=tk.LEFT, padx=(8, 0))


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
    """Carrega o ícone e força tamanho 16x16. Usa Pillow se disponível; senão, subsample."""
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
            ph = PhotoImage(file=str(icon_path))
            w, h = ph.width(), ph.height()
            if w > 16 or h > 16:
                fx = max(1, w // 16)
                fy = max(1, h // 16)
                ph = ph.subsample(fx, fy)
            return ph
    except Exception:
        return None