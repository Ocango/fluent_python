from math import hypot
class Vector():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        #%r就是调用对象的__repr__
        return 'Vector(%r, %r)' % (self.x,self.y)

    def __abs__(self):
        #平方根
        return hypot(self.x,self.y)
    
    def __bool__(self):
        # return bool(abs(self))
        return bool(self.x or self.y)

    def __add__(self ,other):
        # +
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def __mul__(self, scalar):
        # *
        return Vector(self.x * scalar,self.y * scalar)

vector = Vector(3,4)
other = Vector(1,1)
print(vector)
print(abs(vector))
if vector:
    print("True")
print(vector + other)
print(vector * 3)
# print(3 * vector)
# error,不支持反向运算