import tkinter as tk
import globalpy
from common_tk import build

globalpy.root = tk.Tk()
globalpy.root.title("NinjaFiles")
globalpy.root.geometry("350x625")
globalpy.root.configure(bg='#1c1c1c')
build()

globalpy.root.mainloop()