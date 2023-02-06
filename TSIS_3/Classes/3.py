class Shape:
    def Area():
        return 0

class Rectagle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.width*self.length

width = int(input())
length = int(input())
r1 = Rectagle(width, length)
print(r1.area())