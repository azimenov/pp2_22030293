from math import tan
num_sides = int(input())
length = int(input())

def to_radians(degree):
    return 3.14*degree/180

print(length**2*num_sides*tan(to_radians(180/num_sides))/4)