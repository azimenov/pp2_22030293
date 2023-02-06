import math
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Show(self):
        return [self.x, self.y]

    def Move(self, delta):
        self.x += delta
        self.y += delta
        return [self.x, self.y]

    def Dist(self, x2, y2):
        return math.sqrt((self.x - x2)**2+(self.y - y2)**2)
 
x = int(input())
y = int(input())
p1 = Point(x, y)
print(p1.Show())
print(p1.Move(6))
print(p1.Dist(0, 0))