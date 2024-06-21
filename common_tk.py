import tkinter as tk
import globalpy

from settings_tk import settings
from external_tk import *
from aes_form_tk import *
from local_tk import *
from common_tk2 import clear_window

import sys
sys.path.append('file')
from file import *
from sftp import *

sys.path.append('crypt')
from crypt import *

def configure_scroll_region(event):
    canvas.config(scrollregion=canvas.bbox('all'))

def build(file = "", mode = ""):
    global canvas
    global button_frame
    global input1
    global button_exist
    button_exist = 0

    input1 = tk.Entry(globalpy.root, bg="#292929", fg="#FFFFFF")
    input1.pack(fill=tk.X, padx=10, pady=10, ipadx=5, ipady=5)
    input1.bind("<Key>", on_entry_change)

    dirPath = "./db"
    files_in_dir = ldir(dirPath)

    frame = tk.Frame(globalpy.root, borderwidth=0)
    frame.pack()

    canvas = tk.Canvas(frame, width=325, height=500, bg='#292929', highlightthickness=0)  # Usunięcie widocznego obramowania z canvas
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    button_frame = tk.Frame(canvas)
    canvas.create_window(canvas.winfo_width()//2, canvas.winfo_height()//2, window=button_frame, anchor='center')  # Centrowanie ramki
    
    if mode == 2:
        for item in sftp_list:
            print("item" + item)
            if file == "":
                item_frame = tk.Frame(button_frame, borderwidth=0)
                item_frame.pack(fill=tk.X)

                button = tk.Button(item_frame, text=f"{item}", width=20, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: external_note_view(item))
                button.pack(side=tk.LEFT, padx=5, pady=5)

                minus_button = tk.Button(item_frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: external_minus_button_clicked(item))
                minus_button.pack(side=tk.LEFT, padx=5, pady=5)

                plus_button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: external_plus_button_clicked(item))
                plus_button.pack(side=tk.LEFT, padx=5, pady=5)
            else:
                print(item) 
                if item == file:
                    item_frame = tk.Frame(button_frame, borderwidth=0)
                    item_frame.pack(fill=tk.X)

                    button = tk.Button(item_frame, text=f"{item}", width=20, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: external_note_view(item))
                    button.pack(side=tk.LEFT, padx=5, pady=5)

                    minus_button = tk.Button(item_frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: external_minus_button_clicked(item))
                    minus_button.pack(side=tk.LEFT, padx=5, pady=5)

                    plus_button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: external_plus_button_clicked(item))
                    plus_button.pack(side=tk.LEFT, padx=5, pady=5)

    else:
        for item in files_in_dir:
            if file == "":
                item_frame = tk.Frame(button_frame, borderwidth=0)
                item_frame.pack(fill=tk.X)

                button = tk.Button(item_frame, text=f"{item}", width=20, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: fileEntry(item))
                button.pack(side=tk.LEFT, padx=5, pady=5)

                minus_button = tk.Button(item_frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: minus_button_clicked(item))
                minus_button.pack(side=tk.LEFT, padx=5, pady=5)

                plus_button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: plus_button_clicked(item))
                plus_button.pack(side=tk.LEFT, padx=5, pady=5)
            else:
                print(item)
                for f in file:
                    if item == f:
                        item_frame = tk.Frame(button_frame, borderwidth=0)
                        item_frame.pack(fill=tk.X)

                        button = tk.Button(item_frame, text=f"{item}", width=20, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: fileEntry(item))
                        button.pack(side=tk.LEFT, padx=5, pady=5)

                        minus_button = tk.Button(item_frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: minus_button_clicked(item))
                        minus_button.pack(side=tk.LEFT, padx=5, pady=5)

                        plus_button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: plus_button_clicked(item))
                        plus_button.pack(side=tk.LEFT, padx=5, pady=5)
        


    canvas.bind("<Configure>", configure_scroll_region)

    settings_button = tk.Button(globalpy.root, text="settings", bg="#000000", fg="#FFFFFF", command=settings)
    settings_button.pack(side=tk.LEFT, padx=5, pady=5)

    local_button = tk.Button(globalpy.root, text="local", bg="#000000", fg="#FFFFFF", command=local)
    local_button.pack(side=tk.LEFT, padx=5, pady=5)

    external_button = tk.Button(globalpy.root, text="external", bg="#000000", fg="#FFFFFF", command=external_password_view)
    external_button.pack(side=tk.LEFT, padx=5, pady=5)

    if mode == 2:
        button = tk.Button(globalpy.root, text="+", bg="#000000", fg="#FFFFFF", command=lambda: add_element(2))
    else:
        button = tk.Button(globalpy.root, text="+", bg="#000000", fg="#FFFFFF", command=add_element)
    button.pack(side=tk.LEFT, padx=5, pady=5)


def add_element(mode = ''):
    global button_exist
    global button_frame  
    global canvas  
    if button_exist == 1:
        print("Element already exists")
    else:
        item_frame = tk.Frame(button_frame)
        item_frame.pack(fill=tk.X)

        entry = tk.Entry(item_frame, width=31, relief="ridge", bg="#1c1c1c", fg="#FFFFFF")
        entry.pack(side=tk.LEFT, anchor='center', padx=5, pady=0)

        if mode == 2:
            button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda entry=entry: external_on_submit(entry))
            button.pack(side=tk.LEFT, anchor='center', padx=5, pady=0)
        else:
            button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda entry=entry: on_submit(entry))
            button.pack(side=tk.LEFT, anchor='center', padx=5, pady=0)

        button_exist = 1

        button_frame.update_idletasks()  # Zaktualizuj elementy widgetów przed zmianą rozmiaru
        current_height = button_frame.winfo_height()
        new_height = current_height + 20
        button_frame.config(height=new_height)

        canvas.update_idletasks()  # Zaktualizuj elementy widgetów przed zmianą rozmiaru
        current_height = canvas.winfo_height()
        new_height = current_height + 20
        canvas.config(height=new_height)




def matching_find_file(search_string, search_directory='.'):
    matching_files = []
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if search_string.lower() in file.lower():
                matching_files.append(file)  
    return matching_files

def on_entry_change(event):
    global input1
    global previous_text
    current_text = input1.get() 
    
    if event.char.isalpha():
        print("Litera została wpisana. Tekst w polu Entry: {} Litera: {}".format(current_text, event.char))
        file_name = current_text + event.char
        result = matching_find_file(file_name, "./db")
        #result = find_file(file_name)
        print(result)

        if result is not None:
            print(result)
            clear_window()
            build(result)
            input1.insert(0, file_name)
            input1.focus_set()
            

    previous_text = current_text


def back(item = ''):
    print(item)
    clear_window()
    build()



def local():
    clear_window()
    build()

def external():
    global external_password_input
    global aes_pass
    global aes_correct
    global sftp_list 

    key = ''
    if globalpy.aes_correct == 1:
        key = aes_pass
    else:
        key = globalpy.external_password_input.get()
        key = b'' + key.encode('utf-8')
        aes_pass = key

    data = read_file_data("./keys/config.sftp")
    config_sftp = aes_dec(data, key)
    config_sftp_array = config_sftp.split('\n')

    for line in config_sftp_array:
        print(line)
    
    aes_correct = 1    
    sftp_list = list_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4])
    clear_window()
    build("", 2)

    #list_file_sftp()
    #aes_dec("./sftp/config.sftp")


def plus_button_clicked(item):
    global aes_pass
    global aes_correct
    global sftp_list 
    
    print(aes_pass)
    if(aes_pass != ''):
        try:
            key = aes_pass
            data = read_file_data("./keys/config.sftp")
            config_sftp = aes_dec(data, key)
            config_sftp_array = config_sftp.split('\n')
            print(config_sftp_array)
            connection_successful = check_connection(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3])
            print(connection_successful)
            if connection_successful:
                upload_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], "./db/" +  item , config_sftp_array[4] + "/" + item)
        except Exception as e:
            print("An error occurred while reading and decrypting the config file:", e)