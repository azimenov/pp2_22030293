import sys
def gen(n):
    for i in range(n):
        yield i**2
 
n = int(input())
for i in gen(n):
    print(i)

