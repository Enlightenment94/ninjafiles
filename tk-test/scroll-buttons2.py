import tkinter as tk

root = tk.Tk()
root.geometry("300x300")

canvas = tk.Canvas(root, bg="#1c1c1c")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = tk.Frame(canvas, bg="#1c1c1c")  
canvas.create_window((0,0), window=frame, anchor='nw')

def minus_button_clicked(item):
    print(f"Minus button clicked for {item}")

files_in_dir = ["File1", "File2", "File3", "File4", "File5", "File6", "File7", "File8", "File9", "File10"]

for item in files_in_dir:
    button = tk.Button(frame, text=f"{item}", width=27, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: print(item))
    button.pack(side=tk.TOP, anchor='center', padx=5, pady=5)
    
    minus_button = tk.Button(frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: minus_button_clicked(item))
    minus_button.pack(side=tk.RIGHT, anchor='e', padx=5, pady=5)

canvas.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()