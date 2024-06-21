import tkinter as tk
import globalpy
import common_tk
import common_tk2

def external_on_submit(entry):
    global root
    global button_exist
    global sftp_list
    print(entry.get())
    item = entry.get()

    data = read_file_data("./keys/config.sftp")
    config_sftp = aes_dec(data, aes_pass)
    config_sftp_array = config_sftp.split('\n')

    for line in config_sftp_array:
        print(line)

    create_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], item, '')
            
    sftp_list = list_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4])

    common_tk2.clear_window()

    common_tk.build("", 2)
    button_exist = 0


def external_minus_button_clicked(item):
    clear_window()
    global root
    label = tk.Label(globalpy.root, text=f"Are you sure you want to delete from external {item}?")
    label.pack()

    frame = tk.Frame(globalpy.root)
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
        data = read_file_data("./keys/config.sftp")
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
            data = read_file_data("./keys/config.sftp")
            config_sftp = aes_dec(data, aes_pass)
            config_sftp_array = config_sftp.split('\n')

            for line in config_sftp_array:
                print(line)

            download_file_sftp(config_sftp_array[0], config_sftp_array[1], config_sftp_array[2], config_sftp_array[3], config_sftp_array[4], item, './db/' + item)


def external_note_view(item):
    global root
    global text_editor
    global pharse_password
    global pharse_password_entry
    print("external_note_view")
    clear_window()
    
    item_frame = tk.Frame(globalpy.root)
    item_frame.pack(fill=tk.X)

    pharse_password_entry = tk.Entry(globalpy.root, show='*')
    pharse_password_entry.insert(0, pharse_password)
    pharse_password_entry.pack()

    text_editor = tk.Text(globalpy.root, width=325, height=500)
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
    
    scrollbar = tk.Scrollbar(globalpy.root, command=text_editor.yview)
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
        data = read_file_data("./keys/config.sftp")
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
        data = read_file_data("./keys/config.sftp")
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