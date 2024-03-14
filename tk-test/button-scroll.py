import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# Tworzenie ramki do umieszczenia przycisków
frame = tk.Frame(root)
frame.pack()

# Tworzenie przewijanej ramki
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Dodawanie paska przewijania do przewijanej ramki
scrollbar = tk.Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)

# Tworzenie ramki dla przycisków
button_frame = tk.Frame(canvas)
canvas.create_window(0, 0, window=button_frame, anchor='nw')

# Dodawanie przycisków do ramki
for i in range(20):
    button = tk.Button(button_frame, text=f"Button {i}")
    button.pack()

# Konfiguracja przewijanej ramki po zmianie rozmiaru okna
def configure_scroll_region(event):
    canvas.config(scrollregion=canvas.bbox('all'))

canvas.bind("<Configure>", configure_scroll_region)

root.mainloop()