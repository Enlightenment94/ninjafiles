import paramiko

def list_file_sftp(hostname, username, password, port, path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password, port=port)
    sftp_client = ssh_client.open_sftp()
    remote_folder_path = path
    file_list = sftp_client.listdir(remote_folder_path)
    print("Lista plików w folderze:", remote_folder_path)
    for file_name in file_list:
        print(file_name)

    sftp_client.close()
    ssh_client.close()
    return file_list

def check_connection(hostname, username, password, port):
    ssh_client = paramiko.SSHClient()
    try:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, password=password, port=port)
        ssh_client.close()
        return True
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print("Unable to establish SSH connection:", e)
    except paramiko.BadHostKeyException as e:
        print("Host key could not be verified:", e)
    except Exception as e:
        print("An error occurred:", e)

    return False

def upload_file_sftp(hostname, username, password, port, local_path, remote_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password, port=port)
    sftp_client = ssh_client.open_sftp()
    
    print("Przesyłanie pliku", local_path, "do", remote_path)
    sftp_client.put(local_path, remote_path)
    
    sftp_client.close()
    ssh_client.close()

def delete_file_sftp(hostname, username, password, port, path, file_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname, port=port, username=username, password=password)
    sftp = client.open_sftp()

    sftp.chdir(path)

    file_exists = False
    try:
        sftp.stat(file_name)
        file_exists = True
    except IOError:
        print(f"File '{file_name}' not found in path '{path}'")

    if file_exists:
        sftp.remove(file_name)
        print(f"File '{file_name}' successfully deleted")

    sftp.close()
    client.close()

def download_file_sftp(hostname, username, password, port, path, file_name, local_path):
    # Tworzenie obiektu klienta SFTP
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Nawiązanie połączenia
    client.connect(hostname, port=port, username=username, password=password)
    sftp = client.open_sftp()

    # Przejście do określonej ścieżki
    sftp.chdir(path)

    # Sprawdzenie, czy podany plik istnieje
    file_exists = False
    try:
        sftp.stat(file_name)
        file_exists = True
    except IOError:
        print(f"File '{file_name}' not found in path '{path}'")
        sftp.close()
        client.close()
        return
    
    # Pobranie pliku
    sftp.get(file_name, local_path)
    print(f"File '{file_name}' downloaded to '{local_path}'")

    # Zamknięcie połączenia
    sftp.close()
    client.close()

def create_file_sftp(hostname, username, password, port, path, file_name, content):
    port = int(port)
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        sftp.stat(path)
    except FileNotFoundError:
        sftp.mkdir(path)
    
    with sftp.file(f"{path}/{file_name}", "w") as file:
        file.write(content)
    
    sftp.close()
    transport.close()

def download_file_to_variable_sftp(hostname, username, password, port, path, file_name):
    try:
        transport = paramiko.Transport((hostname, int(port)))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        file_size = sftp.stat(path + "/" + file_name).st_size
        if file_size > 32 * 1024 * 1024:
            print("File size exceeds 32MB. Cannot download.")
            return None

        with sftp.file(path + "/" + file_name, 'rb') as file:
            file_content = file.read()
        
        sftp.close()
        transport.close()

        return file_content

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None