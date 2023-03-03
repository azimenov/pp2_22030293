import re
text = 'Do you want to install, the rec.'
pattern = '[ ,.]'
x = re.sub(pattern, ':', text)
print(x)