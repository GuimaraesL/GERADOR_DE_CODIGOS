import ttkbootstrap as ttk
from ui.gui import App as GuiApp

print("Iniciando aplicação...")

try:
    root = ttk.Window(themename="flatly")
    print("Instância Tk criada.")
    GuiApp(root)
    print("App carregado.")
    root.mainloop()
    print("Loop encerrado.")
except Exception as e:
    print("Erro ao iniciar a interface:", e)