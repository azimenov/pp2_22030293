class Shape:
    def Area():
        return 0

class Square(Shape):
    def __init__(self , length):
        self.length = length

    def Area(self):
        return (self.length*self.length)

a = int(input())
print(Shape.Area())
sq1 = Square(a)
print(sq1.Area())

    