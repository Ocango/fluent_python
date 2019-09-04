from fractions import Fraction
class ArithmeticProgression():
    def __init__(self,start,step,end = None):
        self.start = start
        self.step = step
        self.end = end
    
    def __iter__(self):
        result = type(self.start +self.step)(self.start)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.start + self.step * index

ap = ArithmeticProgression(0,Fraction(2,3))
index = 0
for name in ap:
    print(name)
    if index > 10 :
        break
    index += 1