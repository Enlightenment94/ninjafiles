import tkinter as tk
import globalpy
import common_tk2
import common_tk

def external_password_view():
    global aes_correct
    global external_password_input
    global root
    common_tk2.clear_window()
    if globalpy.aes_correct == 1:
        external()
    else:
        label = tk.Label(globalpy.root, text="Enter your SFTP password:")
        globalpy.external_password_input = tk.Entry(globalpy.root, show='$')
        button = tk.Button(globalpy.root, text="Connect", command=common_tk.external)
        globalpy.external_password_input.insert(0, "strong_ABCD!0123")

        label.pack()
        globalpy.external_password_input.pack()
        button.pack()

        label.config(text="Enter your SFTP password:")

        back_button = tk.Button(globalpy.root, text="<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=common_tk.back)
        back_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5) 