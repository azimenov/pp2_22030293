import re
text_to_search = input()
pattern = re.compile(r'ab*')
matches = pattern.finditer(text_to_search)
for match in matches:
    print(match)
