import ttkbootstrap as ttk

# Temas populares do ttkbootstrap (escolha os que preferir)
AVAILABLE_THEMES = [
    "flatly", "cosmo", "darkly", "cyborg", "morph",
    "pulse", "sandstone", "solar", "superhero", "yeti", "zephyr"
]

def apply_theme(theme_name: str = "flatly") -> ttk.Style:
    """
    Aplica o tema informado e retorna o objeto Style (para uso/ajustes).
    Se o tema não existir, cai no padrão do ttkbootstrap.
    """
    try:
        style = ttk.Style(theme_name)
    except Exception:
        style = ttk.Style()  # fallback
    _tweak_base_styles(style)
    return style

def _tweak_base_styles(style: ttk.Style):
    """
    Pequenos ajustes visuais (tipografia/espacamento).
    Evita configs muito agressivas para manter compatibilidade.
    """
    try:
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10, "italic"))
        style.configure("Card.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
        style.configure("Card.TLabelframe", padding=10)
        style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"))
        style.configure("TButton", padding=6)
    except Exception:
        pass