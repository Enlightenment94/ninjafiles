import tkinter as tk

import globalpy
from common_tk2 import *
import common_tk

import sys
sys.path.append('crypt')
import PyCrypt

def noteView(item):
    global root
    global text_editor
    global pharse_password
    global pharse_password_entry
    print("NoteView")
    clear_window()
    
    item_frame = tk.Frame(globalpy.root)
    item_frame.pack(fill=tk.X)

    globalpy.pharse_password_entry = tk.Entry(globalpy.root, show='*')
    globalpy.pharse_password_entry.insert(0, globalpy.pharse_password)
    globalpy.pharse_password_entry.pack()

    text_editor = tk.Text(globalpy.root, width=325, height=500)
    text_editor.config(font=("Arial", 8))

    button = tk.Button(item_frame, text=f"encrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: wenc(item))
    button.pack(side=tk.LEFT, padx=(5,0), pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"decrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: wdec(item, globalpy.pharse_password_entry))
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"pass", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=on_entry_change_pharse_key)
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')

    button = tk.Button(globalpy.root, text=f"<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: common_tk.back(item))
    button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    text_editor.pack()
    
    scrollbar = tk.Scrollbar(globalpy.root, command=text_editor.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_editor.config(yscrollcommand=scrollbar.set)


def wenc(item):
    global text_editor
    global decrypt_flag
    selected_file = "./db/" + item
    if globalpy.decrypt_flag == 1:
        area = text_editor.get("1.0", "end-1c").rstrip()
        encoded_bytes = area.encode()
        enc("./keys/public_key.pem", encoded_bytes, selected_file)
    else:
        print("Blocked text not loaded !!!")

def wdec(item, entry):
    global text_editor
    global decrypt_flag
    file_path = "./db/" + item
    pharsekey = entry.get()
    try:
        content = PyCrypt.dec("./keys/private_key.pem", file_path, pharsekey)
        text_editor.delete('1.0', tk.END)
        text_editor.insert(tk.END, content) 
        globalpy.decrypt_flag = True
    except Exception as e:
        print("Decryption failed:", str(e)) 

def on_entry_change_pharse_key():
    global pharse_password
    global pharse_password_entry
    current_text = globalpy.pharse_password_entry.get() 
    globalpy.pharse_password = current_text 

def fileEntry(item):
    print(item)
    noteView(item)

def yes_clicked(item):
    remove_file(item)
    clear_window()
    build()

def no_clicked():
    clear_window()
    build()


def minus_button_clicked(item):
    clear_window()
    global root
    label = tk.Label(globalpy.root, text=f"Are you sure you want to delete {item}?")
    label.pack()

    frame = tk.Frame(globalpy.root)
    frame.pack()

    yes_button = tk.Button(frame, text="Yes", command=lambda: yes_clicked(item), bg="darkblue", fg="white")
    yes_button.pack(side=tk.LEFT)

    no_button = tk.Button(frame, text="No", command=no_clicked, bg="darkred", fg="white")
    no_button.pack(side=tk.RIGHT)


def on_submit(entry):
    global root
    global button_exist
    print(entry.get())
    file_name = "./db/" + entry.get()
    create_file(file_name)
    
    clear_window()
    build()
    button_exist = 0