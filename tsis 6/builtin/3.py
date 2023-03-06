string = input()
new_string = ''.join(reversed(string))
if string == new_string:
    print("True")