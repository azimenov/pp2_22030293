my_list = [1, 2, 3, 4, 5]
with open ('text.txt', 'w') as f:
    for item in my_list:
        f.write(str(item)+ ' \n')