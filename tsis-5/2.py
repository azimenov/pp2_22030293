import re
def task2(text):
    pattern = 'ab{2,3}'
    x = re.findall(pattern, text)
    try:
        print(x)
    except AttributeError as e:
        print("Not found")
