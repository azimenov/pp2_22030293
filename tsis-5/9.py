import re
text = input()
pattern = '[A-Z][^A-Z]*'
x = re.findall(pattern, text)
for i in x:
    print(i + " ", end='')