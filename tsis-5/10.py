import re
text = input()
pattern = '[A-Z][^A-Z]*'
x = re.findall(pattern, text)
res = ""
for i in x:
    res += i.lower() + "_"
print(res)