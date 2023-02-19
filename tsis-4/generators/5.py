def my_gen(n):
    num = n
    while num >= 0 :
        yield num
        num -= 1

for i in my_gen(7):
    print(i)