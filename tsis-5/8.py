import re
text = input()
pattern = re.compile(r'[A-Z][^A-Z]')

x = re.findall(pattern, text)
for match in x:
    print(match, end = ' ')
