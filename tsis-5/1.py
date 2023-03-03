import re
def task1(text):
    pattern = 'ab*'
    x = re.search(pattern, text)
    print(x.start())

