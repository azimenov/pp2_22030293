import os

os.chdir('C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6')
for dirpath, dirnames, filenames in os.walk('C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6'):
    print(dirnames)

print()

for dirpath, dirnames, filenames in os.walk('C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6'):
    print(filenames)

print()

for dirpath, dirnames, filenames in os.walk('C:/Users/Сулпак/OneDrive/Документы/pp2/tsis 6'):
    print(dirnames)
    print(filenames)
    print()
