import tkinter as tk

from common_tk2 import clear_window
import globalpy
import common_tk

def settings():
    clear_window()

    # Label and Entry for SFTP server address
    sftp_address_label = tk.Label(globalpy.root, text="SFTP Server Address:")
    sftp_address_label.pack()
    sftp_address_entry = tk.Entry(globalpy.root)
    sftp_address_entry.pack()

    # Label and Entry for SFTP username
    sftp_username_label = tk.Label(globalpy.root, text="SFTP Username:")
    sftp_username_label.pack()    
    sftp_username_entry = tk.Entry(globalpy.root)
    sftp_username_entry.pack()

    sftp_password_label = tk.Label(globalpy.root, text="SFTP Password:")
    sftp_password_label.pack()
    sftp_password_entry = tk.Entry(globalpy.root,show='*')
    sftp_password_entry.pack()

    # Label and Entry for AES password
    aes_password_label = tk.Label(globalpy.root, text="AES Password:")
    aes_password_label.pack()
    aes_password_entry = tk.Entry(globalpy.root, show='*')
    aes_password_entry.pack()

    port = tk.Label(globalpy.root, text="PORT:")
    port.pack()
    port_entry = tk.Entry(globalpy.root) 
    port_entry.pack()

    path_entry = tk.Label(globalpy.root, text="Path:")
    path_entry.pack()
    path_entry = tk.Entry(globalpy.root) 
    path_entry.pack()

    save_button = tk.Button(globalpy.root, text="Save", command=lambda: save_settings
    (sftp_address_entry.get(), sftp_username_entry.get
    (), sftp_password_entry.get(), aes_password_entry.get(), port_entry.get
    (), path_entry.get() )) 
    save_button.pack()

    button = tk.Button(globalpy.root, text=f"<", width=5, height=2, relief="ridge", bg="#1c1c1c", fg="#FFFFFF", command=back_settings)
    button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

def save_settings(sftp_address, sftp_username, sftp_password, aes_password, port, path):
    try:
        if not os.path.exists('./keys'):
            os.makedirs('./keys')

        key = b'' + aes_password.encode()
        file_to_encrypt = './keys/config.sftp'

        data = sftp_address + "\n" + sftp_username + "\n" + sftp_password + "\n"  + port + "\n" + path
        enc_data = aes_enc(data, key)
        writeDataToFile(enc_data, file_to_encrypt)

        print("Saved Settings\n", f"SFTP Server Address: {sftp_address}\nSFTP Username: {sftp_username}\nPort: {port}\nPath: {path}")
    except Exception as e:
        print("Error saving setting2s:", e)


def back_settings():
    clear_window()
    common_tk.build()
