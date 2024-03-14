import os

def ldir(path):
    files_list = []
    if os.path.isdir(path):
        files_list = os.listdir(path)
    else:
        print("Not a folder.")
    
    return files_list

def create_file(filename):
    if os.path.exists(filename):
        print(f"Warning: File with name '{filename}' already exists.")
    else:
        with open(filename, 'w') as file:
            print(f"File '{filename}' created successfully.")

def remove_file(filename):
    file_path = "./db/" + filename

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Plik {file_path} został usunięty.")
    else:
        print("Plik nie istnieje.")

def find_file(file_name):
    folder_path = "./db/"
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            return file_path
    return None    

def writeDataToFile(data, file_path):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print(f"Data has been successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing data to {file_path}: {str(e)}")

def read_file_data(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    return data

def check_exist(file_path):
    if os.path.exists(file_path):
        print(f"File '{file_path}' exists")
        return 1
    else:
        print(f"File '{file_path}' not found")
        return 0
