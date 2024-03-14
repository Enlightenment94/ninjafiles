import tkinter as tk
from file import *
from sftp import *
# importing module

import sys
sys.path.append('crypt')
from PyCrypt import *

#global war
root = 0
button_exist = 0
button_frame = 0
text_editor  = 0
decrypt_flag = 0
previous_text= 0
input1       = 0
external_password_input = 0
pharse_password = ''
pharse_password_entry = 0
aes_pass = ''
aes_correct = 0
sftp_list = ''

def configure_scroll_region(event):
    canvas.config(scrollregion=canvas.bbox('all'))

def keyView():
    print("KeyView")

def build(file = "", mode = ""):
    global canvas
    global button_frame
    global input1
    global button_exist
    button_exist = 0

    input1 = tk.Entry(root, bg="#292929", fg="#FFFFFF")
    input1.pack(fill=tk.X, padx=10, pady=10, ipadx=5, ipady=5)
    input1.bind("<Key>", on_entry_change)

    dirPath = "./db"
    files_in_dir = ldir(dirPath)

    frame = tk.Frame(root, borderwidth=0)
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
                if item == file:
                    item_frame = tk.Frame(button_frame, borderwidth=0)
                    item_frame.pack(fill=tk.X)

                    button = tk.Button(item_frame, text=f"{item}", width=20, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: fileEntry(item))
                    button.pack(side=tk.LEFT, padx=5, pady=5)

                    minus_button = tk.Button(item_frame, text="-", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: minus_button_clicked(item))
                    minus_button.pack(side=tk.LEFT, padx=5, pady=5)

                    plus_button = tk.Button(item_frame, text="+", width=3, relief="ridge", bg="#000000", fg="#FFFFFF", command=lambda item=item: plus_button_clicked(item))
                    plus_button.pack(side=tk.LEFT, padx=5, pady=5)
        


    canvas.bind("<Configure>", configure_scroll_region)

    settings_button = tk.Button(root, text="settings", bg="#000000", fg="#FFFFFF", command=settings)
    settings_button.pack(side=tk.LEFT, padx=5, pady=5)

    local_button = tk.Button(root, text="local", bg="#000000", fg="#FFFFFF", command=local)
    local_button.pack(side=tk.LEFT, padx=5, pady=5)

    external_button = tk.Button(root, text="external", bg="#000000", fg="#FFFFFF", command=external_password_view)
    external_button.pack(side=tk.LEFT, padx=5, pady=5)

    if mode == 2:
        button = tk.Button(root, text="+", bg="#000000", fg="#FFFFFF", command=lambda: add_element(2))
    else:
        button = tk.Button(root, text="+", bg="#000000", fg="#FFFFFF", command=add_element)
    button.pack(side=tk.LEFT, padx=5, pady=5)

def settings():
    clear_window()

    # Label and Entry for SFTP server address
    sftp_address_label = tk.Label(root, text="SFTP Server Address:")
    sftp_address_label.pack()
    sftp_address_entry = tk.Entry(root)
    sftp_address_entry.pack()

    # Label and Entry for SFTP username
    sftp_username_label = tk.Label(root, text="SFTP Username:")
    sftp_username_label.pack()    
    sftp_username_entry = tk.Entry(root)
    sftp_username_entry.pack()

    sftp_password_label = tk.Label(root, text="SFTP Password:")
    sftp_password_label.pack()
    sftp_password_entry = tk.Entry(root,show='*')
    sftp_password_entry.pack()

    # Label and Entry for AES password
    aes_password_label = tk.Label(root, text="AES Password:")
    aes_password_label.pack()
    aes_password_entry = tk.Entry(root, show='*')
    aes_password_entry.pack()

    port = tk.Label(root, text="PORT:")
    port.pack()
    port_entry = tk.Entry(root) 
    port_entry.pack()

    path_entry = tk.Label(root, text="Path:")
    path_entry.pack()
    path_entry = tk.Entry(root) 
    path_entry.pack()

    save_button = tk.Button(root, text="Save", command=lambda: save_settings
    (sftp_address_entry.get(), sftp_username_entry.get
    (), sftp_password_entry.get(), aes_password_entry.get(), port_entry.get
    (), path_entry.get() )) 
    save_button.pack()

    button = tk.Button(root, text=f"<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=back_settings)
    button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

def save_settings(sftp_address, sftp_username, sftp_password, aes_password, port, path):
    try:
        if not os.path.exists('./sftp'):
            os.makedirs('./sftp')

        key = b'' + aes_password.encode()
        file_to_encrypt = './sftp/config.sftp'

        data = sftp_address + "\n" + sftp_username + "\n" + sftp_password + "\n"  + port + "\n" + path
        enc_data = aes_enc(data, key)
        writeDataToFile(enc_data, file_to_encrypt)

        print("Saved Settings\n", f"SFTP Server Address: {sftp_address}\nSFTP Username: {sftp_username}\nPort: {port}\nPath: {path}")
    except Exception as e:
        print("Error saving setting2s:", e)

def back_settings():
    clear_window()
    build()

def local():
    clear_window()
    build()



def external_password_view():
    global aes_correct
    global external_password_input
    global root
    clear_window()
    if aes_correct == 1:
        external()
    else:
        label = tk.Label(root, text="Enter your SFTP password:")
        external_password_input = tk.Entry(root, show='$')
        button = tk.Button(root, text="Connect", command=external)
        external_password_input.insert(0, "strong_ABCD!0123")

        label.pack()
        external_password_input.pack()
        button.pack()

        label.config(text="Enter your SFTP password:")

        back_button = tk.Button(root, text="<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=back_settings)
        back_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5) 





def external():
    global external_password_input
    global aes_pass
    global aes_correct
    global sftp_list 

    key = ''
    if aes_correct == 1:
        key = aes_pass
    else:
        key = external_password_input.get()
        key = b'' + key.encode('utf-8')
        aes_pass = key

    data = read_file_data("./sftp/config.sftp")
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

def external_minus_button_clicked(item):
    clear_window()
    global root
    label = tk.Label(root, text=f"Are you sure you want to delete from external {item}?")
    label.pack()

    frame = tk.Frame(root)
    frame.pack()

    yes_button = tk.Button(frame, text="Yes", command=lambda: external_minus_button_clicked_confirmation(item), bg="darkblue", fg="white")
    yes_button.pack(side=tk.LEFT)

    no_button = tk.Button(frame, text="No", command=no_clicked, bg="darkred", fg="white")
    no_button.pack(side=tk.RIGHT)

def external_minus_button_clicked_confirmation(item):
    global external_password_input
    global aes_pass
    global aes_correct
    global sftp_list 

    if aes_pass != '':
        data = read_file_data("./sftp/config.sftp")
        config_sftp = aes_dec(data, aes_pass)
        config_sftp_array = config_sftp.split('\n')

        for line in config_sftp_array:
            print(line)

        delete_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], item)
            
        sftp_list = list_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4])

    clear_window()
    build("", 2)


def external_plus_button_clicked(item):
    flag = check_exist("./db/" + item)
    if(flag == 0):
        if aes_pass != '':
            data = read_file_data("./sftp/config.sftp")
            config_sftp = aes_dec(data, aes_pass)
            config_sftp_array = config_sftp.split('\n')

            for line in config_sftp_array:
                print(line)

            download_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], item, './db/' + item)





def on_entry_change(event):
    global previous_text
    current_text = input1.get() 
    
    if event.char.isalpha():
        print("Litera została wpisana. Tekst w polu Entry: {} Litera: {}".format(current_text, event.char))
        file_name = current_text + event.char
        result = find_file(file_name)
        print(result)
        if result is not None:
            print(result)
            clear_window()
            build(file_name)
            

    previous_text = current_text

def fileEntry(item):
    print(item);
    noteView(item)

def clear_window():
    global root
    for widget in root.winfo_children():
        widget.destroy()




def yes_clicked(item):
    remove_file(item)
    clear_window()
    build()

def no_clicked():
    clear_window()
    build()

def plus_button_clicked(item):
    global external_password_input
    global aes_pass
    global aes_correct
    global sftp_list 
    
    print(aes_pass)
    if(aes_pass != ''):
        try:
            key = aes_pass
            data = read_file_data("./sftp/config.sftp")
            config_sftp = aes_dec(data, key)
            config_sftp_array = config_sftp.split('\n')
            print(config_sftp_array)
            connection_successful = check_connection(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3])
            print(connection_successful)
            if connection_successful:
                upload_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], "./db/" +  item , config_sftp_array[4] + "/" + item)
        except Exception as e:
            print("An error occurred while reading and decrypting the config file:", e)

def minus_button_clicked(item):
    clear_window()
    global root
    label = tk.Label(root, text=f"Are you sure you want to delete {item}?")
    label.pack()

    frame = tk.Frame(root)
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


def external_on_submit(entry):
    global root
    global button_exist
    global sftp_list
    print(entry.get())
    item = entry.get()

    data = read_file_data("./sftp/config.sftp")
    config_sftp = aes_dec(data, aes_pass)
    config_sftp_array = config_sftp.split('\n')

    for line in config_sftp_array:
        print(line)

    create_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], item, '')
            
    sftp_list = list_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4])

    clear_window()

    build("", 2)
    button_exist = 0
    #Stwórz plik
    #Stwórz listę na nowo 

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





def noteView(item):
    global root
    global text_editor
    global pharse_password
    global pharse_password_entry
    print("NoteView")
    clear_window()
    
    item_frame = tk.Frame(root)
    item_frame.pack(fill=tk.X)

    pharse_password_entry = tk.Entry(root, show='*')
    pharse_password_entry.insert(0, pharse_password)
    pharse_password_entry.pack()

    text_editor = tk.Text(root, width=325, height=500)
    text_editor.config(font=("Arial", 8))

    button = tk.Button(item_frame, text=f"encrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: wenc(item))
    button.pack(side=tk.LEFT, padx=(5,0), pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"decrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: wdec(item, pharse_password_entry))
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"pass", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=on_entry_change_pharse_key)
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')

    button = tk.Button(root, text=f"<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: back(item))
    button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    text_editor.pack()
    
    scrollbar = tk.Scrollbar(root, command=text_editor.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_editor.config(yscrollcommand=scrollbar.set)

def on_entry_change_pharse_key():
    global pharse_password
    global pharse_password_entry
    current_text = pharse_password_entry.get() 
    pharse_password = current_text 

def back(item):
    print(item)
    clear_window()
    build()

def wdec(item, entry):
    global text_editor
    global decrypt_flag
    file_path = "./db/" + item
    pharsekey = entry.get()
    try:
        content = dec("./keys/private_key.pem", file_path, pharsekey)
        text_editor.delete('1.0', tk.END)
        text_editor.insert(tk.END, content) 
        decrypt_flag = True
    except Exception as e:
        print("Decryption failed:", str(e)) 

def wenc(item):
    global text_editor
    global decrypt_flag
    selected_file = "./db/" + item
    if decrypt_flag == 1:
        area = text_editor.get("1.0", "end-1c").rstrip()
        encoded_bytes = area.encode()
        enc("./keys/public_key.pem", encoded_bytes, selected_file)
    else:
        print("Blocked text not loaded !!!")



def external_note_view(item):
    global root
    global text_editor
    global pharse_password
    global pharse_password_entry
    print("external_note_view")
    clear_window()
    
    item_frame = tk.Frame(root)
    item_frame.pack(fill=tk.X)

    pharse_password_entry = tk.Entry(root, show='*')
    pharse_password_entry.insert(0, pharse_password)
    pharse_password_entry.pack()

    text_editor = tk.Text(root, width=325, height=500)
    text_editor.config(font=("Arial", 8))

    button = tk.Button(item_frame, text=f"encrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: external_wenc(item))
    button.pack(side=tk.LEFT, padx=(5,0), pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"decrypt", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: external_wdec(item, pharse_password_entry))
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')
    
    button = tk.Button(item_frame, text=f"pass", width=4, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=on_entry_change_pharse_key)
    button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, anchor='n')

    button = tk.Button(root, text=f"<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=lambda item=item: external_back(item))
    button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    text_editor.pack()
    
    scrollbar = tk.Scrollbar(root, command=text_editor.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_editor.config(yscrollcommand=scrollbar.set) 

def external_back(item):
    print(item)
    clear_window()
    build('',2)

def external_wdec(item, entry):
    global text_editor
    global decrypt_flag
    #file_path = "./db/" + item
    pharsekey = entry.get()
    try:
        data = read_file_data("./sftp/config.sftp")
        config_sftp = aes_dec(data, aes_pass)
        config_sftp_array = config_sftp.split('\n')

        for line in config_sftp_array:
            print(line)

        #content = dec("./keys/private_key.pem", file_path, pharsekey)
        file_name = item
        content = download_file_to_variable_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], file_name)
        
        content = dec_from_varrable("./keys/private_key.pem", content, pharsekey)

        text_editor.delete('1.0', tk.END)
        text_editor.insert(tk.END, content) 
        decrypt_flag = True
    except Exception as e:
        print("Decryption failed:", str(e)) 

def external_wenc(item):
    global text_editor
    global decrypt_flag
    selected_file = "./db/" + item
    if decrypt_flag == 1:
        data = read_file_data("./sftp/config.sftp")
        config_sftp = aes_dec(data, aes_pass)
        config_sftp_array = config_sftp.split('\n')

        for line in config_sftp_array:
            print(line)
        
        area = text_editor.get("1.0", "end-1c").rstrip()
        encoded_bytes = area.encode()
        encrypted = enc_to_varriable("./keys/public_key.pem", encoded_bytes)
        file_name = item
        create_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], file_name, encrypted)
    else:
        print("Blocked text not loaded !!!")


root = tk.Tk()
root.title("NinjaFiles")
root.geometry("350x625")
root.configure(bg='#1c1c1c')
build()

root.mainloop()