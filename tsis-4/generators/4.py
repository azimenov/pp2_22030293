def squares(a, b):
    while b >= a:
        yield b**2
        b -= 1

for i in squares(1, 4):
    print(i)