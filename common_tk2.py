import globalpy

def clear_window():
    for widget in globalpy.root.winfo_children():
        widget.destroy()