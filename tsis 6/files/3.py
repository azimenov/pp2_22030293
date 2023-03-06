import os

path = 'C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6/files'

if os.path.exists(path):
    print('exists')
    print(f"Filename: {os.path.basename(path)}")
    print(f"Directory: {os.path.dirname(path)}")
else:
    print('doesnt exist')