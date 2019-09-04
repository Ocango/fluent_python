#切片
s = 'bicycle'
print(s[::-2])
#切片这是一种对__getitem__的操作

#切片对文本的操作
text = """
1909  Order Book        $12.00  3   $13.66
1206  Error like me     $11.20  1    $2.99
"""
Description = slice(6,24)
Unit_Price = slice(24,32)
line_items = text.split('\n')[1:]
for item in line_items:
    print(item[Description],item[Unit_Price])

#给切片赋值
l = list(range(10))
l[3::2] = [11,22,33,44]
print(l)
l[2:5] = []
print(l)

#序列+，*

#序列+=，*=

#一个奇怪的现象
t = (1,2,[10,20])
print(id(t))
t[2].extend([30,40])
# t[2] += [50,60]
# t[2] = t[2] + [50,60]
#这样会引发异常，元组不可变？
print(id(t))
print(t)
#元组可变？

#已排序队列的搜索
import bisect
# bisect(haystact,needle)
# haystact中查找needle的位置,这个查找是保证比needle小都在haystact之前.要求haystact已排序
bisect.bisect_left
#比较有趣的用法
def grade(score,breakpoints = [60,70,80,90],grades = 'FDCBA'):
    i = bisect.bisect_right(breakpoints,score)
    return grades[i]
print([grade(score) for score in [33,60,62,69,80,100]])

#已排序队列的插入
bisect.insort_left([],10)