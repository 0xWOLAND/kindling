import math


class Rotate:
    def __init__(self, x, y, deg):
        self.x = x
        self.y = y
        self.deg = deg

    def rotate(self):
        deg = self.deg_to_rad()
        X = float(self.x * math.cos(deg) + self.y * math.sin(deg))
        Y = float(self.y * math.cos(deg) - self.x * math.sin(deg))
        return [X, Y]

    def deg_to_rad(self):
        return self.deg * math.pi / 180


r = Rotate(2, 6, 60)
print("Rotated vals are:  ({}, {})".format(r.rotate()[0], r.rotate()[1]))
sum_x = 1 + math.sqrt(27)
sum_y = 3 - math.sqrt(3)
print("sum_x:   {0}\nsum_y:    {1}\n".format(sum_x,sum_y))
if r.rotate()[0] is sum_x and r.rotate()[1] is sum_y:
    print("The solution is correct")
else:
    print("the solution is incorrect")