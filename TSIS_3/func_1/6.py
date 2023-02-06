def reverser(str1):
    my_list = list(str1.split())
    result = ""
    for i in my_list[::-1]:
        result += i+' '
    return result
print(reverser("abb 551"))