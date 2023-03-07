import re
text = input()
pattern = re.compile(r'[A-Z][^A-Z]*')

matches = pattern.finditer(text)

for match in matches:
    print(match)
