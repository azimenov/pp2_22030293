import os
from datetime import datetime

path = 'C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6/files'
if os.access(path, os.F_OK):
    print(f"{path} exists")
else:
    print(f"{path} does not exist")

if os.access(path, os.R_OK):
    print(f"{path} is readable")
else:
    print(f"{path} is not readable")

if os.access(path, os.W_OK):
    print(f"{path} is writable")
else:
    print(f"{path} is not writable")

if os.access(path, os.X_OK):
    print(f"{path} is executable")
else:
    print(f"{path} is not executable")