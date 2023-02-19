def my_gen(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

n = int(input())
for i in my_gen(n):
    print(i)