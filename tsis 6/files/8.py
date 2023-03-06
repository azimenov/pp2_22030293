import os

path = 'C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6/files/text.txt'
if os.path.exists(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print(f"{path} deleted successfully.")
    else:
        print(f"{path} is not writable. Cannot delete file.")
else:
    print(f"{path} does not exist.")