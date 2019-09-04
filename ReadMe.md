# 说明
本项目基于Luciano Ramalho的《Fluent Python》，属于个人练习。
# Section1 Python 的数据类型
## 双下方法
__len__(self):#len()
__getitem__(self,mark):#items[i]
__init__(self):#item = Item()
__repr__(self):#print(item)
__abs__(self):#abs(item)
__bool__(self):#if item:
__add__(self ,other):#item + other
__mul__(self, scalar):#item * scalar
## 序列
### 列表推导
[i for i in range(10)]
### 生成器表达式
(i for i in range(10))
### 拆包
a,b = b,a
### 切片
l[::-2]
l[:5] = []
### 序列的增量赋值
m = l*5
m += [1,2]

### 一个奇怪的现象
```
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
```
### sorted(lists)与list.sort()
区别sorted会新建列表作为返回值
而list.sort只是对当前list进行操作
### 已排序搜索和插入
```
#比较有趣的用法
def grade(score,breakpoints = [60,70,80,90],grades = 'FDCBA'):
    i = bisect.bisect_right(breakpoints,score)
    return grades[i]
print([grade(score) for score in [33,60,62,69,80,100]])

#已排序队列的插入
bisect.insort_left([],10)
```
## 数组
```
from array import array
from random import random
floats = array('d',(random()*100 for i in range(10**7)))
print(floats[-1])
#注意哦，数组里面存的是数字的字节表达
fp = open('floats.bin','wb')
floats.tofile(fp)
fp.close()
```
### 内存视图memoryview
泛化和去数学化的NumPy数组，实现在数据结构之间共享内存。用以处理大型数据集合
注意共享内存的意思是对memoryview的操作不会产生新的对象！！！这也是其高效的原因
### NumPy 与 SciPy
```
from time import perf_counter as pc
t0 = pc()
floats = numpy.loadtxt('data.txt')
t1 = pc()
floats /= 3
t2 = pc()
numpy.save('floats-10M',floats)
t3 = pc()
floats2 = numpy.load('floats-10M.npy','r+')
t4 = pc()
floats2 *=363
t5 = pc()
{'t0': 0.851668039, 't1': 153.021685987, 't2': 153.038698158, 't3': 153.4188989, 't4': 153.420616467, 't5': 153.455011833}
```
读取txt和二进制文件简直天壤之别，当然这有NumPy优化内存映射机制
## 队列
```
from collections import deque
dq = deque(range(10),maxlen = 10)
dq.rotate(-4)
print(dq)
dq.pop()
print(dq)
dq.extend([11,12,13])
print(dq)
```
### queue
```
import queue
#用以同步线程安全，满员时会等待销毁后再执行
```
### multiprocessing
```
import multiprocessing
#用以同步进程管理，同queue
```
### asyncio
```
import asyncio
#是用来编写 并发 代码的库，使用 async/await 语法
```
### heapq
import heapq
```
#将可变序列当做堆队列处理
```
## 基本数据类型对象
int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple
## 字典dict
### 字典推导
{country : code for code,country in [(1,'China'),(2,'EN')]}
### setdefault
index.setdefault(word,[]).append(location)
word不存在赋值[]，然后接着执行
### __missing__
```
dd = defaultdict(list)
mm = defaultdict(lambda : '<missing>')
```
这个方法只对__getitem__()有效
### update()
将可迭代对象批量更新进去，作用同merge
### OrderedDict
有序的键
### ChainMap
组合多个字典
### Counter
键带计数器
### UserDict
标准的dict用来自定义dict
### MappingProxyType
映射只读实例
d_proxy = MappingProxyType({})
## 集合
集合去重无序
支持很多中缀运算符  |合集   &交集   -差集
集合可以类比数学运算符
&   |   -   ^   in  <=  <   >=  >
### 散列表
![散列表原理](.\hash_table.png)
而dict和set都是可散列的，简单点说，他们的键都是不可重复的，原因可以看如下
```
def __hash__(self):
    return hash(id(self))
def __eq__(self, other):
    if isinstance(other, self.__class__):
        return hash(id(self))==hash(id(other))
    else:
        return False  
```
由此__eq__的定义我们也能知道为什么可哈希集合？==？
散列表的问题在于内存开销巨大
另外在散列表中新增会导致重新分配内存。同时迭代与更新散列表是一件危险的事
## 字符
str对象中获得的元素都是Unicode字符
何为字符：
以4~6个十六进制数表示码位
字符的具体表述取决于其编码，编码是在码位和字节序列转换用的算法
### 编码规范申明
```
#!/usr/bin/python
# -*- coding:utf-8 -*-
```
### 编码解码
Unicode字符     encode 编码     字节序列
                decode 解码

### 字节序标记byte-order mark
编码的前置标识，用来标识编码方式，以及识别编码

### 处理文本文件
- 尽早解码成字符串
- 处理过程中尽量不进行编码和解码
- 编码输出文本
！open file时始终明确编码，因为open文件时使用的是默认系统编码
！推举：chardet进行编码测试
### 编码默认值
在open文件时：系统默认编码
在输出输入控制台时：控制台的编码
而python3系统内部：使用utf-8
### 为了比较Unicode字符
```
from unicodedata import normalize
'''
NFC     最小码位都成等价字符
NFD     拆解成基字符的组合字符
这两个会把兼容字符分解成兼容分解字符，
会曲解原意但有利于将单字符解析成有意义的多字符
NFKC    
NFKD
'''
def nfc_equal(str1,str2):
    retrun normalize('NFC',str1) == normalize('NFC',str2)
```
### 大小写折叠
str.casefold()
类似str.lower()，但是其规范了一些特殊符号的大小写问题

通过上述两个函数进行Unicode规范化和大小写折叠都是符合Unicode标准的
### 去掉变音符号
```
import string
import unicodedata
def shave_marks(txt):
    '''
    去掉变音符号
    '''
    norm_txt = unicodedata.normalize('NFD',txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    #combining返回规范组合类,无组合类则为0
    return unicodedata.normalize('NFC',shaved)
```

### 转换
str.maketrans转换对照表，用于str.translate

### Unicode排序算法实现
pyuca.Collator.sort_key

### 双模式API
import re,os
为了处理str和bytes不同情况

# Section2 将函数视为对象
## 一等函数
### __doc__()
帮助文档
### 将函数视为对象
```
def factorial(n):
    """return factorial n!"""
    return 1 if n<2 else n * factorial(n-1)

print(factorial.__doc__)

fact = factorial
print(list(map(fact,range(11))))
```
### 高阶函数
如上文的map，正在被生成器表达式替代
### 匿名函数
lambda
```
sorted(fruits,key = lambda word : word[::-1])
```
### 可调用对象
用户定义的函数
def/lambda
内置函数
len/time.strftime
内置方法
dict.get
方法

类
__new__()
类的实例
__call__()
生成器函数
yield

可以通过callable(obj)确认对象是否可以调用
只要任何对象实现__call__()即可表现的像函数

### 函数内省
dir(class) #探知属性
__dict__() #注解
__annotations__() #参数和返回值的注解
__call__() #实现()运算符
__defaults__ #形式参数的默认值
__code__() #编译成字节码的函数元数据和函数定义体

### 参数
定位参数、关键字参数、仅限关键字参数
### 调用函数前进行参数验证
```
from inspect import signature
signature 的 bind 方法
```
### 函数注解
```
def clip(text:str,max_len:'int > 0' = 10) -> str:
    """
    最长max_len后截断空格
    """
```

### 函数式编程
operator#标准运算符替代函数
```
'''
operator.mul(a,b)
#return a * b
'''

'''
g = operator.itemgetter(*index)
g(obj) === obj[index] if len(index) == 1 else (obj(a) for a in index)
#return obj[index] if len(index) == 1 else (obj(a) for a in index)
#多于一个返回元组
'''

'''
g = operator.attrgetter(*name)
g(obj) === obj[name] if len(name) == 1 else (obj.a for a in name)
#return obj[name] if len(name) == 1 else (obj.a for a in name)
#可以根据.深入嵌套对象，获得指定元素
'''

'''
g = operator.methodcaller(name,*args,**kwargs)
g(b) === b.name(*args,**kwargs)
#返回一个可调用对象!
'''
```
运算	|	Syntax	|	Function
:-: | :-: | :-:
Addition	|	a + b	|	add(a, b)
Concatenation	|	seq1 + seq2	|	concat(seq1, seq2)
Containment Test	|	obj in seq	|	contains(seq, obj)
Division	|	a / b	|	truediv(a, b)
Division	|	a // b	|	floordiv(a, b)
Bitwise And	|	a & b	|	and_(a, b)
Bitwise Exclusive Or	|	a ^ b	|	xor(a, b)
Bitwise Inversion	|	~ a	|	invert(a)
Bitwise Or	|	a | b	|	or_(a, b)
Exponentiation	|	a ** b	|	pow(a, b)
Identity	|	a 是 b	|	is_(a, b)
Identity	|	a 不是 b	|	is_not(a, b)
Indexed Assignment	|	obj[k] = v	|	setitem(obj, k, v)
Indexed Deletion	|	del obj[k]	|	delitem(obj, k)
Indexing	|	obj[k]	|	getitem(obj, k)
Left Shift	|	a << b	|	lshift(a, b)
Modulo	|	a % b	|	mod(a, b)
Multiplication	|	a * b	|	mul(a, b)
Matrix Multiplication	|	a @ b	|	matmul(a, b)
Negation (Arithmetic)	|	- a	|	neg(a)
Negation (Logical)	|	not a	|	not_(a)
Positive	|	+ a	|	pos(a)
Right Shift	|	a >> b	|	rshift(a, b)
Slice Assignment	|	seq[i:j] = values	|	setitem(seq, slice(i, j), values)
Slice Deletion	|	del seq[i:j]	|	delitem(seq, slice(i, j))
Slicing	|	seq[i:j]	|	getitem(seq, slice(i, j))
String Formatting	|	s % obj	|	mod(s, obj)
Subtraction	|	a - b	|	sub(a, b)
Truth Test	|	obj	|	truth(obj)
Ordering	|	a < b	|	lt(a, b)
Ordering	|	a <= b	|	le(a, b)
Equality	|	a == b	|	eq(a, b)
Difference	|	a != b	|	ne(a, b)
Ordering	|	a >= b	|	ge(a, b)
Ordering	|	a > b	|	gt(a, b)

functools
```
'''
functools.reduce
#将可迭代对象第一二个参数传入，return和第三个作为下一个参数，依次往复
'''

'''
functools.partial
#用于部分应用一个函数，即创建一个新的可调用对象，但把函数部分参数固定。这个方法其实在于有些方法可能有些固定参数，比如传入'NFC'格式化字符串，可以提前传入以创建nfc函数
from operator import mul
from functools import partial
triple = partial(mul,3)
list(map(triple,range(1,10)))
'''
```

## 设计模式
### 迭代 策略模式
定义一系列算法，把他们一一封装起来，并使得他们可以互相替换。本模式使得算法可以独立于使用它的客户而变化
![策略模式](.\picture\strategy.png)
### 迭代 命令模式
抽象命令、继承抽象命令 实例化命令接受者 实现具体命令、定义命令接受者 接受者具体实现方法、定义命令调用者 
最后客户端实例化命令接受者、命令调用者，通过命令接受者实例化命令，命令调用者再执行具体命令。
![命令模式](.\picture\command.png)

这两者都因为Python把函数作为一等对象，所以我们可以不给调用者\算法一个实际的对象，直接给函数就好。

```
对接口编程，而不是对实例编程
优先实现对象组合，而不是类继承
```

# Section3 decorator&closure
## what
装饰器相当于用装饰器调用被装饰的函数
同时装饰器在函数**定义/导入**以后立刻运行
## 用装饰器优化策略模式
```
promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promo_func

@promotion
def fidelity(order):
    pass
#在导入时即可填充promos
```
## 变量作用域
当需要让解释器将函数体内变量作为全局变量
需要在函数体内标记global

## 闭包
一般情况下，如果一个函数结束，函数的内部所有东西都会释放掉，还给内存，局部变量都会消失。但是如果满足闭包的条件，外函数在结束的时候发现有自己的临时变量将来会在内部函数中用到，就把这个临时变量绑定给了内部函数，然后自己再结束。
这种临时变量叫做自由变量，整个外函数则形成了闭包。

这里有一个问题要解决：不可变类型不会自觉变成自由变量，需要（因为不可变变量会自觉隐式创建局部变量）
## nonlocal申明
在内部函数内部声明nonlocal,说明不是局部变量

## 装饰器：输出函数运行时间
```
import time
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed,name,arg_str,result))
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n<2 else n * factorial(n-1)

print('*'*40 , 'Calling snooze(.123)')
snooze(.123)
print('*'*40 , 'Calling factorial(6)')
print('6! = ',factorial(6))
```
动态的给一个对象增加一些额外的责任
迭代

```
import functools
def clock2(func):
    @functools.wraps(func)
    def clocked(*args,**kwargs):
        t0 = time.time()
        result = func(*args,**kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k,w) for k,w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.append(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed,name,arg_str,result))
    return clocked
```
functools.wraps将func中__name__&__doc__属性复刻到clocked中（保留原函数的属性，装饰器毕竟会将原函数替换为内函数），协助构建行为良好的装饰器
## 标准库的装饰器
### functools.lru_cache()
备忘功能，可以将耗时的函数结果保存下来，以防止传入相同的参数重复计算
最常见的参考就是斐波那契了
```
@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2 :
        return n
    return fibonacci(n-2) + fibonacci(n-1)

print(fibonacci(30))
```
参数maxsize指定缓存多少个结果,参数typed会区分不同参数类型，比如1和1.0

### 单分派泛函数functools.singledispatch
因为python不支持重载，所以带来了它
根据第一个参数的类型选择专门的函数
## 叠放装饰器
## 参数化装饰器
工厂函数。怎么让装饰器接受其他参数呢？那就让装饰器装饰装饰器
**定义一个装饰器工厂函数，返回装饰器**
### 参数化clock
更新并返回表示当前本地符号表的字典。 在函数代码块但不是类代码块中调用 locals() 时将返回自由变量。 请注意在模块层级上，locals() 和 globals() 是同一个字典。

# Section4 面向对象
对象在赋值之前就创建了
## 标识，相等性，别名
每个变量都有标识、类型、值，对象一旦建立，他的标识就不会变，is比较对象的标识，id()返回对象标识的整数标识
## 元组的相对不可变性
即元组的数据结构的物理内容不可变（即保存的引用不可变）
，但是引用的可变对象的值还是可变的
## 默认做浅复制
利用构造方法和切片创建的多数内置可变集合都是浅复制
即复制了外部容器，但是内部的引用还是不变的。
## 深复制和浅复制
import copy
同时通过__copy__()&__deepcopy__()定义copy和deepcopy的行为
## python只支持共享传参！
即函数内部的形式参数是实参的中各个引用的副本（浅复制哦）
## 避免将可变类型作为参数发的默认值
来看多图警告：

![直接指向可变对象](.\picture\直接指向可变对象.png)
![直接指向可变对象的结果](.\picture\直接指向可变对象的结果.png)

问题在于python中存在__init__.__default__寄存默认值，可变变量作为默认值在加载模块式就已经确定了，直接用，危险危险！
比较好的办法就是用**利用构造方法和切片创建的多数内置可变集合进行浅复制**代替等号这种直接赋值的方法
## del和对象回收
> 对象绝对不会自行销毁；然而无法获得对象时，可能会被当做垃圾回收。
```
#演示一个回调函数
import weakref
s1 = {1,2,3}
s2 = s1
def bye():
    print('GOODBYE!')

ender = weakref.finalize(s1,bye)
print(ender.alive)
del s1#不会删除对象
print(ender.alive)
s2 = 'spam'#重新绑定最后一个引用导致{1,2,3}无法获取，则对象被销毁
print(ender.alive)
```
### 弱引用
其实示例中s1的引用也在ender中，但是为什么还是被回收了？——>弱引用不会增加引用数量

正是因为有引用，对象才会在内存中存在。在缓存中，弱引用保证被缓存引用的对象不因此而始终保存
### weekref.ref获取所指对象
### weekref.WeakKeyDictionary实现可变映射
里面的值是对象的弱引用
但是不是所有的对象都可以作为弱引用的目标
一些更加邪道的特性就不多说了，涉及到编辑器的实现

# Section5 duck type,python风格的对象
## classmethod
定义类方法
## staticmethod
定义构造方法
## 格式化显示
__format__()
优化处理：
```
    def angle(self):
        return math.atan2(self.y,self.x)
    def __format__(self, format_spec = ''):
        #优化下：可以解析以p结尾的格式化语句，以转化为极坐标系
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self),self.angle())
            outer_fmt = '<{},{}>'
        else:
            coords = self
            outer_fmt = '({},{})'
        components = (format(c,format_spec) for c in coords)
        return outer_fmt.format(*components)
```
## 可散列
### 只读特性
使用两个前导下划线把属性标记为私有
```
    def __init__(self, x=0, y=0):
        self.__x = float(x)
        self.__y = float(y)
    
    @property#将读值属性标记为特性
    def x(self):#读值属性与公开属性同名
        return self.__x#直接返回__x
    
    @property
    def y(self):
        return self.__y
```
### __eq__()
### __hash__()
推荐使用异或混合各分量的散列值

要点其实就是可散列要求是键不可变、相同的键要hash相同、再实现hash，以上即三点所要求的的

## 私有属性，受保护的属性
python不支持直接定义私有属性，通过将python的属性定义为有两个前导下划线的属性名，python会自觉的将此属性归类到实例的__dict__中，并且前面还会加上```_type(self).__name__```例如如下：_Vector__x
以此防止子类覆盖私有属性：简单点说就是没有私有属性这个概念，而是投机取巧，只能预防
所以其实是可以通过```_Vector__x```去修改`私有属性`的值
所以其实在python中大家约定俗成的使用_单个前导下划线去自行约束自己的行为，虽然编译器不会去辅助你，但你可以辅助自己

## __slots__属性
在类中定义slots后，实例将不会有除了slots中的其他东西
但是__slots__确实是一种优化手法，有利于节省内存

## 覆盖类属性
类属性实例可以直接调用修改，这样就变成实例自己的属性了
但是更好的方法是
### 继承子类
简单点说就是前面的问题，用子类去覆盖父类的属性

## 精彩直至
![利用反射打破私有](.\picture\利用反射打破私有.png)

# Section6 序列的修改、散列和切片
之前就有涉猎，python中创建完善的序列不需要使用继承，只需要符合序列协议的方法。这有点像建立在低级语言与编译器交互的逻辑上，但是却是使用的非正式的接口
序列主要的两个方法就是__len__()与__getitem__()

所以，因为行为想序列，所以我们才说他是序列，这就是python中所谓的鸭子模型

## 可切片的序列
### 切片的实现原理
dir(slice)
help(indices)
S.indices(len) ——> (start,stop,stride)
```这也是切片为嘛要知道len的原因```
### 实现切片返回Vector对象
```
    def __getitem__(self,index):
        '''
        这个内容审查可以参阅：
        class Myseq:
            def __getitem__(self,index):
                return index
        从而查看index的行为
        '''
        cls = type(self)
        if isinstance(index,slice):
            return cls(self._components[index])#切片是返回slice
        elif isinstance(index,numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))
```
## 动态存取属性
属性查找失败时，解释器会调用__getattr__方法
所以传说中的只读属性可以通过一种另类的方法来体现
### 问题：setattr
但是上述的问题，这种不存在的属性，影响了赋值的体现，即看得到，能赋值，但是没有效果(不存在的值会被记录为此对象类属性)
所以我们需要setattr避免异常表现
```
    def __setattr__(self,name,value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortname_names:
                error = 'Readonly attribute {attr_name!r}'
            elif name.islower():
                error = "Can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name = cls.__name__,attr_name = name)
                raise AttributeError(msg)
        super().__setattr__(name,value)
```
所以基本上__getattr__定义了，也要__setattr__以保证行为一致
## 散列
一样，求异或

# Section7 接口，从协议到抽象基类
协议让python对象在系统中扮演特定的角色
## 回到我们的扑克类
原先的扑克类是一个不可变序列，因为我们没有__setitem__
所以我们可以在运行时补上
```
def set_card(deck,position,card):
    deck._cards[position] = card

FrenchDeck.__setitem__ = set_card
shuffle(deck)
```
我们将这种模式叫做猴子补丁
由此我们亦可以看出我们的协议是动态的，他并不在乎你的类型是啥，只要对象实现了对应的可变序列协定即可

## 这是一个大家庭
### collections.abc
![collections.abc](.\picture\collections.abc.png)
- Iterable,Container,Sized

基本所有人要实现的协议，主要体现在__iter__()支持迭代,__contains__()支持in运算符,__len__()支持len函数
- Sequence,Mapping,Set

不可变集合，Mutablexxx是他们可变的子类
- MappingView

.item(),.keys()和.values()返回的分别是ItemView、KeysView、ValuesView的实例

- Callable,Hashable

为内置函数isinstance提供支持，以一种安全的方法判断对象能否散列

- Iterator

Iterable的子类

### 抽象基类的数字塔
import numbers
- Number
- Complex
- Real
- Rational
- Integral

## 继承
首先有个问题，内置类型的方法不会调用子类覆盖的方法，比如dict的子类覆盖了__getitem__()，其不会被内置类型的get()方法调用
所以子类化内置类型有各种各样的问题，所以，请子类化collections模块
## 多重继承的解析顺序
### 类的__mro__属性
其记录了循序的超类解析顺序
### 调用超类的方法
```
super().ping()#利用super()
A.ping(self)#直接在类上调用方法传入实例
```
### 一些祷告
- 把接口继承和实现继承区分开
- 使用抽象基类显式表示接口
- 通过混入重用代码Mixin
- 在名称中明确指明混入
- 抽象基类可以作为混入，反之不可
- 不要子类化多个具体类
- 为用户提供聚合类
- 优先使用对象组合，而不是类继承

# Section8 运算符重载
## 一元运算符
### -(__neg__)负运算符
### +(__pos__)正运算符
### ~(__invert__)位取反
### abs(__abs__)绝对值
## 什么是a+b
### 实现基本的加法运算符
```
def __add__(self,other):
    pairs = itertools.zip_longest(self,other,fillvalue = 0.0)
    return Vector(a+b for a,b in pairs)
```
### 那么b+a呢？
a+b的检查顺序：检查a有__add__，检查b有__radd__
那么投机取巧下：
```
def __radd__(self,other):
    return self+other
```
### 异常处理
主要是要处理TypeError，让编译器尝试准备反转运算符再抛出NotImplemented
```
def __add__(self,other):
    try:
        pairs = itertools.zip_longest(self,other,fillvalue = 0.0)
        return Vector(a+b for a,b in pairs)
    except TypeError:
        return NotImplemented
```
## 什么是a*b
这里我们采用白鹅类型处理
```
def __mul__(self,scalar):
    if isinstance(scalar,numbers.Real):
        return Vector(n*scalar for n in self)
    else:
        return NotImplemented
def __rmul__(self,scalar):
    return self * scalar
```
## 其他的运算符
注意哦，a+b的检查顺序应用到了很多运算符。比如==，同时还有后备机制（都不行时），同时也有一个问题，要返回NotImplemented才会继续检查下去
![比较运算符](.\picture\比较运算符.png)
这其实一个问题，程序员讨厌惊喜

# Section9 控制流程
迭代器，生成器，牛皮。一定程度避免了直接生成结果导致资源的极度浪费
## 单词序列
序列可以迭代的原因
当解释器需要迭代对象时，会自动调用iter()
而内置的iter行为如下
1.检查对象是否实现了__iter__,若果实现就调用并返回一个迭代器
2.如果没有，就调用__getitem__从零开始自行迭代
3.如果还是不行，那就返回TypeError

这种查询方式就是经典的鸭子类型，如果换成白鹅类型，如下：
只检查__iter__的实现，因为Iterable实现了__subclasshook__，默认包揽所有实现__iter__就不用大家去继承抽象基类Iterable了

而实际Iterator的实现由两部分组成：*__next__()*,__iter__()

__next__返回下一个对象，如果没有则返回StopIteration异常

__iter__返回迭代器返回本身
## 可迭代对象
明确可迭代对象返回一个迭代器的设计理念，而不是即是又是
## 用生成器函数代替返回一个迭代器的设计理念
### 生成器函数
只要python函数体有yield,那么他就是生成器函数，调用它时会返回一个生成器对象

生成器和之前提到的概念一致
```
def gen_123():
    yield 1
    yield 2
    yield 3
> gen_123
<function gen_123 at 0x0000000003A29D90>
> gen_123()
<generator object gen_123 at 0x0000000003A69840>
```
生成器其实是截断函数的执行(第一次执行才是开始，不是停在第一个yield)，待启动时，才会继续执行，这一点和装饰器差距很大

### 惰性实现：生成器表达式、生成器函数
即不要急于实现
## 等差数列生成器
### 自己的类
```
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
```
### 生成器函数
就是把上文class的__iter__拆出来了，不说话
### itertools模块
标准库中的生成器
![用于过滤的生成器](.\picture\用于过滤的生成器.png)
![用于映射的生成器](.\picture\用于映射的生成器.png)
![合并多个可迭代对象的生成器](.\picture\合并多个可迭代对象的生成器.png)
![把输入的各个元素拓展成多个输出的生成器](.\picture\把输入的各个元素拓展成多个输出的生成器.png)
![重新排列元素的生成器](.\picture\重新排列元素的生成器.png)

## yield from
新的语法糖，用来调用生成器

## 归约函数
![归约函数](.\picture\归约函数.png)

## 更多有关iter的消息
### iter(可调用对象，哨符)
类似截止符的操作。有一个比较有趣的用法
```
with open('mydata.txt') as fp:
    for line in iter(fp.readline,'\n')
        process_line(roll)
```
### 大佬的操作
[文档解析](https://github.com/fluentpython/isis2json)

# Section10 上下文管理器和else
## else
### if
if为假时
### for
循环完毕时
### while
while条件为假时
### try
没有异常时执行

发现一件事，这本书处处都在批判Guide对于语法糖和添加关键字，唯恐避之不及的态度的抱怨
不过确实是，虽然这种方法减少了语法糖，但是，理解难度也高了

## 上下文管理器
### 基本结构
**__enter__**初始化上下文管理器

**__exit__**无论以任何方式退出上下文管理器都会调用

***注意不要在__exit__再次抛出返回的异常，而是应该返回True||False***
### 示例
示例使用了一个修改print语境的上下文
```
class LookingGlass():
    def __enter__(self):
        import sys 
        self.original_write = sys.stdout.write#保存原write方法
        sys.stdout.write = self.reverse_write#猴子补丁
        return 'JABBERWOCKY'#上下文的返回值
    
    def reverse_write(self,text):#翻转输出
        self.original_write(text[::-1])
    
    def __exit__(self,exc_type,exc_value,traceback):#exc_type异常类，exc_value.args异常实例，有些参数传给异常构造方法，traceback对象，在finally中调用sys.exe_info()得到的就是这三个参数
        import sys
        sys.stdout.write = self.original_write#还原
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero')
            return True
```
保证在此上下文中输出都是反序，结束后再恢复

这里注意print其实就是包装的sys.stdout对象，将参数传递给此对象的write方法
### 使用@contextmanager装饰器定义上下文管理器
通过yield把函数切分开来，前半部分是__enter__，后半部分是__exit__

其实就是把函数包装成了包含__enter__||__exit__的类
```
import contextlib
@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    
    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'#避免用户在with模块瞎玩
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
```
有一点不一样，用此装饰器需要显式抛出异常

# Section11 协程
yield之前在生成器和上下文管理器中讲过，其实yield虽然在这些不同的情况下用法迥异，但是yield其实就是流程控制语句，yield会把时间片交还出去，等待有人来喊他继续执行
## 协程
在生成器API中加入了.send(value)方法，生成器的调用方式可以用.send(...)发送数据，发送数据会成为生成器函数中yield表达式的值。

同时也有.throw(...)调用方抛出异常交给生成器，.close()终止生成器
## 演示
```
def simple_coroutine():
    print('-> coroutine started!')
    x = yield
    print('-> coroutine received :',x)

#使用inspect.getgeneratorstate(...)确定协程的状态
my_coro = simple_coroutine()#'GEN_CREATED'等待开始执行
next(my_coro)#'GEN_RUNNING'解释器正在执行,也可以send(None)督促其执行
#'GEN_SUSPENDED'在yield处暂停
my_coro.send(42)#'GEN_RUNNING'解释器正在执行
#'GEN_CLOSED'执行结束
```
有个小问题，如果是x = yield a ,第一个next会发生什么？

要解决这个问题得明确两件事。当函数中有yield时，他就不是一般的函数了，平时我们写的```simple_coroutine()```并不是执行函数，而是创建了生成器对象。当我们调用```next(...)```或者```.send(...)```时才会开始执行，且是执行到第一个```yield ...```(等号运算符是先执行右边再执行左边)，对于```x = yield a```来说，赋值是没有发生的，只是发生了yield返回了a的值

### 预激协程装饰器
```
from functools import wraps
def coroutine(func):
    """装饰器：向前执行到第一个yield表达式，预先激活'func'"""
    @wraps(func)
    def primer(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer
```
## 终止协程和异常处理
当协程遇到无法处理的异常时，他会将异常向上抛出给```next(...)```或者```.send(...)```的调用方，协程立刻终止(即无法处理的错误下方的逻辑不会处理)，再次调用协程只会受到StopIteration。

以上即基本法，所以当有些我们不希望协程终止的异常发生时||异常发生需要清理工作，需要try...catch...else...finally，去正常的结束协程

## 协程的返回值
协程正常结束时会，会返回StopIteration，似乎我们正常的return并不能解决问题，那么：
```
from collections import namedtuple
Results = namedtuple('Result','count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Results(count,average)

avg = averager()
next(avg)
avg.send(12)
avg.send(32)
avg.send(None)
Traceback (most recent call last):
    StopIteration: Result(count=2, average=22.0)
```
很明显可以看到一个方法：捕获StopIteration异常，StopIteration异常携带了结果
```
try:
    avg.send(None)
excet StopIteration as exc:
    result = exc.value
```
这种方法并不违规，是PEP标准，后面yield from则就是用的这种方式

## yield from 
前面说过，yield from x会把控制权交给x,具体的来说应该是iter(x),但是这样看来，似乎很没有意义？

> 所以yield from 实际的主要作用是打开双向的通道，把最外层调用方与最内层的子生成器连接起来。这样两者可以直接发送和产出值，还可以直接传入异常，而不用在处于中间的协程添加大量的异常处理代码。

这句话并不违背yield from x会把控制权交给x的说法，甚至不违背yield是流程控制语句的特性。yield from同样是在等待，只不过面对的不再是单独的对象，而是一个生成器，yield from在调用方和被调用方中间扮演了通信管道的角色
![委派生成器](.\picture\委派生成器.png)
- 调用方

可以直接通过委派生成器获得子生成器的结果

通过.send(None)通知子生成器结束，同时委派生成器也结束了
- 委派生成器

预激活子生成器

捕获子生成器的StopIteration异常的返回值，同时终结自己（回想前面的所述的yield赋值的问题，如果子生成器不返回StopIteration引导委派生成器退出的话，yield赋值的左边永远不会有值，因为一直没有能轮到赋值语句执行）
- 子生成器

生成器具体逻辑实现
## 案例分析
在大多数的理论体系中，协程是用来在单个线程中管理并发活动的，上述并没有具体体现出来。接下来通过一个示例：离散事件仿真来说明如何使用协程代替线程处理并发
### 离散事件仿真
离散事件模拟将系统随时间的变化抽象成一系列的离散时间点上的事件，通过按照事件时间顺序处理事件来演进，是一种事件驱动的仿真世界观。离散事件仿真将系统的变化看做一个事件，因此系统任何的变化都只能是通过处理相应的事件来实现，在两个相邻的事件之间，系统状态维持前一个事件发生后的状态不变。
### 示例
[开车了](https://github.com/fluentpython/example-code/blob/master/16-coroutine/taxi_sim.py)

# Section12 并发
你觉得并发要了解到什么程度？
> 如何派生出一堆独立的线程，然后用队列收集结果。
## 并发都是因为IO延时
### 网络下载的三种风格
依序下载
```
没啥好说的
```
concurrent.futures模块
```
ThreadPoolExecutor
线程池

submit(fn, *args, **kwargs)
as_completed#传入future，并开始执行，做完会返回

map(func, *iterables, timeout=None, chunksize=1)#依序产生结果

ProcessPoolExecutor
进程池
```
asyncio包
```

```
### 优化版的下载处理
包介绍tqdm
一个进度条工具，根据可迭代对象的__len__和__iter__属性计算可迭代对象的时间

工具Toxiproxy
实际上是一个代理工具，但是又不是简单的进行代理（tcp，可以配置策略，toxics 实现延迟，模拟故障

Celery
任务队列
### threading与multprocessing

## 线程与协程
python中没有终止线程的方法，如果要终止，必须给线程发消息
### threading
```
def superisor():
    signal = Signal()
    spinner  =threading.Thread(target = spin,args = ('thinking!',signal))
    print('spinner object:',spinner)
    spinner.start()#激活线程
    result = slow_function()
    signal.go = False
    spinner.join()#等待线程终止
    return result
```
新版迭代通过threading.Event()控制
```
def supervisor():  # <9>
    done = threading.Event()
    '''
    事件对象
    这是线程之间通信的最简单机制之一：一个线程发出事件信号，而其他线程等待该信号。

    一个事件对象管理一个内部标志，调用 set() 方法可将其设置为true，调用 clear() 方法可将其设置为false，调用 wait() 方法将进入阻塞直到标志为true。

    class threading.Event
    实现事件对象的类。事件对象管理一个内部标志，调用 set() 方法可将其设置为true。调用 clear() 方法可将其设置为false。调用 wait() 方法将进入阻塞直到标志为true。这个标志初始时为false。
    '''
    spinner = threading.Thread(target=spin,
                               args=('thinking!', done))
    '''
    class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)¶
    调用这个构造函数时，必需带有关键字参数。参数如下：

    group 应该为 None；为了日后扩展 ThreadGroup 类实现而保留。

    target 是用于 run() 方法调用的可调用对象。默认是 None，表示不需要调用任何方法。

    name 是线程名称。默认情况下，由 "Thread-N" 格式构成一个唯一的名称，其中 N 是小的十进制数。

    args 是用于调用目标函数的参数元组。默认是 ()。

    kwargs 是用于调用目标函数的关键字参数字典。默认是 {}。

    如果 daemon 不是 None，线程将被显式的设置为 守护模式，不管该线程是否是守护模式。如果是 None (默认值)，线程将继承当前线程的守护模式属性。
    '''
    print('spinner object:', spinner)  # <10>
    spinner.start()  # <11>
    '''
    start()
    开始线程活动。

    它在一个线程里最多只能被调用一次。它安排对象的 run() 方法在一个独立的控制进程中调用。

    如果同一个线程对象中调用这个方法的次数大于一次，会抛出 RuntimeError 。
    '''
    result = slow_function()  # <12>
    done.set()  # <13>
    '''
    set()
    将内部标志设置为true。所有正在等待这个事件的线程将被唤醒。当标志为true时，调用 wait() 方法的线程不会被被阻塞。
    '''
    spinner.join()  # <14>
    '''
    > join(timeout=None)
    等待，直到线程终结。这会阻塞调用这个方法的线程，直到被调用 join() 的线程终结 -- 不管是正常终结还是抛出未处理异常 -- 或者直到发生超时，超时选项是可选的。
    '''
    return result

```
### asyncio
这个鬼迭代的有点快，以官方文档为实例，快速迭代一遍：
#### 入门示例
```
>>> import asyncio

>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')

>>> asyncio.run(main())
hello
world
```
#### 加载协程的方法
1. asyncio.run() 函数用来运行最高层级的入口点 "main()" 函数 (参见上面的示例。)
2. asyncio.create_task() 函数用来并发运行作为 asyncio 任务 的多个协程。
这里面其实涉及两个方面
一个是await直接等待协程方法执行结束
另一个是await asyncio.create_task()对象，从而实现并发
#### 可等待对象的定义
如果一个对象可以在 await 语句中使用，那么它就是 可等待 对象。许多 asyncio API 都被设计为接受可等待对象。

可等待 对象有三种主要类型: 协程, 任务 和 Future.
1. 协程
协程函数: 定义形式为 async def 的函数;
协程对象: 调用 协程函数 所返回的对象。
当然还有基于生成器的老版协程
```
@asyncio.coroutine
def old_style_coroutine():
    yield from asyncio.sleep(1)
```
2. 任务
当一个协程通过 asyncio.create_task() 等函数被打包为一个 任务，该协程将自动排入日程准备立即运行:
3. Future
Future 是一种特殊的 低层级 可等待对象，表示一个异步操作的 最终结果。

当一个 Future 对象 被等待，这意味着协程将保持等待直到该 Future 对象在其他地方操作完毕。

在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码。

通常情况下 没有必要 在应用层级的代码中创建 Future 对象。

Future 对象有时会由库和某些 asyncio API 暴露给用户，用作可等待对象:
```
async def main():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
```
一个很好的返回对象的低层级函数的示例是 loop.run_in_executor()。

#### 方法库
1. 运行 asyncio 程序
asyncio.run(coro, *, debug=False)
此函数运行传入的协程，负责管理 asyncio 事件循环并 完结异步生成器。
当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。

2. 创建任务
asyncio.create_task(coro)
将 coro 协程 打包为一个 Task 排入日程准备执行。返回 Task 对象。

3. 休眠
coroutine asyncio.sleep(delay, result=None, *, loop=None)
阻塞 delay 指定的秒数。
如果指定了 result，则当协程完成时将其返回给调用者。

4. 并发运行任务
awaitable asyncio.gather(*aws, loop=None, return_exceptions=False)
并发 运行 aws 序列中的 可等待对象。

5. 屏蔽取消操作
awaitable asyncio.shield(aw, *, loop=None)
保护一个 可等待对象 防止其被 取消。

6. 超时
coroutine asyncio.wait_for(aw, timeout, *, loop=None)
等待 aw 可等待对象 完成，指定 timeout 秒数后超时。
函数将等待直到目标对象确实被取消，所以总等待时间可能超过 timeout 指定的秒数。

7. 简单等待
coroutine asyncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
并发运行 aws 指定的 可等待对象 并阻塞线程直到满足 return_when 指定的条件。

asyncio.as_completed(aws, *, loop=None, timeout=None)
并发地运行 aws 集合中的 可等待对象。返回一个 Future 对象的迭代器。返回的每个 Future 对象代表来自剩余可等待对象集合的最早结果。

8. 来自其他线程的日程安排
asyncio.run_coroutine_threadsafe(coro, loop)
向指定事件循环提交一个协程。线程安全。
返回一个 concurrent.futures.Future 以等待来自其他 OS 线程的结果。

9. 内省

10. Task 对象
- class asyncio.Task(coro, *, loop=None)
- cancel()
请求取消 Task 对象。
- cancelled()
如果 Task 对象 被取消 则返回 True。
- done()
如果 Task 对象 已完成 则返回 True。
- result()
返回 Task 的结果。
- exception()
返回 Task 对象的异常。

## aiohttp
asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架
### async with
异步上下文管理器”async with”
异步上下文管理器指的是在enter和exit方法处能够暂停执行的上下文管理器。
### 主要示例
```
async def download_many(cc_list):
    async with aiohttp.ClientSession() as session:  # <8>
        res = await asyncio.gather(                 # <9>
            *[asyncio.create_task(download_one(session, cc))
                for cc in sorted(cc_list)])

    return len(res)
```
## 总结一下
其实理论上所有的协程都可以直接把await或者yield from忽视掉。为什么说await后面接的是可等待对象，就是因为await后面接的对象要是暂停了，控制权就会交回事件循环手中，再去驱动其他协程。而为嘛使用了asyncio后我们不再用next(...)或.send(...)了，因为协程的驱动我们交还给了事件循环。甚至在3.7中，事件循环也不显示调用了。

## 更进一步的理解 阻塞性调用
![阻塞性调用](.\picture\阻塞性调用.png)
- 将阻塞性操作交给线程
在线程或者进程池中执行代码。
awaitable loop.run_in_executor(executor, func, *args)
安排在指定的执行器中调用 func 。
```
import asyncio
import concurrent.futures

def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))

async def main():
    loop = asyncio.get_running_loop()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool', result)

asyncio.run(main())
```
## 再来一个方法asyncio.Semaphore
```
semaphore = asyncio.Semaphore(concur_req)#限制并发量的同步装置
```
初始化计数器
semaphore = asyncio.Semaphore(concur_req)

计数器减一
semaphore.acquire()

计数器加一
semaphore.release()

当计数器小于等于零则堵塞协程，或者用async with semaphore:当上下文使用，自动控制
```
    try:
        async with semaphore:#限制并发量
            image = await get_flag(session,base_url,cc)
```
## 聊个天
### 回调地狱
为什么会有yield from ，又为什么会有回调呢？其实这是一个很简单的问题，很远的前方就说过，要预防阻塞性调用，即各种I/O操作对CPU性能的浪费，CPU默默地角落里哭泣，你又让他等硬盘写入，还让他等不知道多久以后才会有返回的TCP链接，CPU心里苦你知道吗！
为什么认为回调是地狱呢？其实回调不管嵌套不嵌套，第一点难以理解，这还好，最大的问题是闭包，这是一个和垃圾回收机制有关的问题，函数调用会在结束时把其作用域没有失去关联的变量全部回收，回调很容易陷入：哎，为嘛取不到变量值？然后设定一大堆全局变量接参的故事。
### 每次循环多个请求
线程版很简单，阻塞线程两次就好了
协程也简单，委托给两个协程就好

## TCP通信模块
server端处理模块
```
async def handle_queries(reader,writer):
    while True:
        writer.write(PROMPT)#StreamWriter.write向流中写入数据
        await writer.drain()#StreamWriter.drain等到适当时再恢复对流的写入
        data = await reader.readline()#StreamReader.readline读一行，其中“line”是以\n。结尾的字节序列。如果收到EOF \n但未找到，则该方法返回部分读取的数据。如果收到EOF且内部缓冲区为空，则返回一个空bytes对象。
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:#处理telnet客户端decode异常，设定为传空字符
            query = '\x00'
        client = writer.get_extra_info('peername')#返回与套接字连接的远程地址
        print('Received from {}: {!r}'.format(client,query))
        if query:
            if ord(query[:1]) < 32:#收到控制字符，退出
                break
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)#将一个列表（或任何可迭代的）字节写入流。
            writer.write(index.status(query,len(lines)).encode() + CRLF)

            await writer.drain()#刷新输出缓冲
            print('Sent {} results'.format(len(lines)))
        
    print('Close the client socket')
    writer.close()
```

# Section13 动态属性和特性
## 动态属性访问JSON类数据
逻辑上很简单，即json对象转化为python原生对象时正常都是dict或者list，我们只能用feed['Schedule'][40]['name']之类的方法去访问dict或者list结构，但是点属性的方式是否更加nice呢？比如feed.Schedule[40].name这样的效果。
所以我们会去构造类的属性获取方法，__getattr__(self,name)，处理dict或者list结构。
```
    @classmethod
    def build(cls,obj):#备选构造方案
        if isinstance(obj,abc.Mapping):#映射对象
            return cls(obj)
        elif isinstance(obj,abc.MutableSequence):#列表对象
            return [cls.build(item) for item in obj]
        else:
            return obj
```
## 处理无效属性名
有一个问题：python保留字导致属性无法访问，比如grad.class
当然我们可以这么做：getattr(grad,'class')

还有一个问题：无效标识符导致属性无法访问（python3可以根据str.isidentifier()判定str是否为有效标识符）
常见的方法是替换为通用名称或者抛出异常

## 使用new方法以灵活的方式创建对象
前面我们是在getattr时，依据不同的值返回不同类型的对象，其实初始化过程中就可以构建对象
```
    def __new__(cls,arg):
        if isinstance(arg,abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg,abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg
```
## shelve模块
俗称架子，一个类似字典，但是值可以是几乎任意python对象，键是字符串，他的背后由dbm支持。
```
def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading '+DB_NAME)
    for collection,res_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in res_list:
            key = '{}.{}'.format(record_type,record['serial'])#定义key值
            record['serial'] = key
            db[key] = Record(**record)
```

更近一步构建关系网
```
# BEGIN SCHEDULE2_RECORD
import warnings
import inspect  # <1>

import osconfeed

DB_NAME = 'data/schedule2_db'  # <2>
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  # 判断属性是否一致，比的是__dict__和归属类
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
# END SCHEDULE2_RECORD


# BEGIN SCHEDULE2_DBRECORD
class MissingDatabaseError(RuntimeError):
    """需要数据库时但是没有指定时抛出."""  # 代替pass语句说明下用途


class DbRecord(Record):  # <2>

    __db = None  # 储存一个打开的shelve.Shelf数据库引用

    @staticmethod  # <4>
    def set_db(db):
        DbRecord.__db = db  # 设置shelve.Shelf数据库引用

    @staticmethod  # <6>
    def get_db():
        return DbRecord.__db #返回shelve.Shelf数据库引用

    @classmethod  # <7>
    def fetch(cls, ident):
        '''获取传入键对应的值'''
        db = cls.get_db()
        try:
            return db[ident]  # 获取对应的键的数据
        except TypeError:
            if db is None:  # <9>
                msg = "database not set; call '{}.set_db(my_db)'"#未设置db
                raise MissingDatabaseError(msg.format(cls.__name__))#说明未设置数据库
            else:  # 非db is None那只能抛出TypeError了
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):  # <11>
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # <12>
# END SCHEDULE2_DBRECORD


# BEGIN SCHEDULE2_EVENT
class Event(DbRecord):  # <1>

    @property#标记对应函数名的读值方法
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)  # 使用继承过来的fetch（舍近求远的原因：预防存在属性fetch）

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):  #属性存在检查
            spkr_serials = self.__dict__['speakers']  # 从__dict__实例中获取属性speakers的值
            fetch = self.__class__.fetch  # <5>
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]  # 将speaker记录列表赋值给_speaker_objs
        return self._speaker_objs  # <7>

    def __repr__(self):
        if hasattr(self, 'name'):  # <8>
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()  # <9>
# END SCHEDULE2_EVENT


# BEGIN SCHEDULE2_LOAD
def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]  # <1>
        cls_name = record_type.capitalize()  # 首字母大写
        cls = globals().get(cls_name, DbRecord)  # 从全局对象中获取名称对应的对象，找不到就用DbRecord
        if inspect.isclass(cls) and issubclass(cls, DbRecord):  # 判断是否是派生类或者子类
            factory = cls  # <5>
        else:
            factory = DbRecord  # 因为如果叫json里面叫event，已经有Event继承DbRecord，就可以用class Event
        for record in rec_list:  # <7>
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # 不过创建的class不太一样了
# END SCHEDULE2_LOAD
```
这个关系网任然是先load_db，但是把event单独归为DbRecord的子类Event,初始load时，因为有些值（单纯的值Event几个只读特性值）在db里面fetch不到，所以存在TypeError，实际全部加载完成时，就有了，同时也多了_speaker_objs属性

蛮复杂，慢慢推理论。
## 特性验证属性
property其实是一个类装饰器，被装饰的方法有一个setter属性，从而绑定读值和设值方法

一种老版的方法，有点像java的set,get
```
# BEGIN LINEITEM_V2B
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):  # <1>
        return self.__weight

    def set_weight(self, value):  # <2>
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)  # <3>

# END LINEITEM_V2B
```
### 特性会覆盖实例属性
前面有个诡异的特例        return self.__class__.fetch(key)  # 使用继承过来的fetch（舍近求远的原因：预防存在属性fetch）

因为特性都是类属性，如果实例有用相同的属性，实例属性就会覆盖类属性，(只是数据表现层面上的，实际你用class.obj还是存在的)

1. 实例属性覆盖类的数据属性
2. 实例属性不会覆盖类特性
3. 新增的类特性覆盖现有实例属性

其实换个说法，当设定特性时，取实例属性，会因为有同名的特性，导致返回的是特性对象。如果同名的不是特性，那还是取实例实际的属性

特性可以从__doc__中获取说明。装饰器直接会显示相关代码，老式方法要传入```doc=''```参数

## 处理属性删除操作
被装饰的方法还有个deleter
```
@member.deleter
def member(self):
    text = "BLACK KNIGHT (loses {})\n-- {}"
    print(text.format(self.members.pop(0)),self.phrases.pop(0))
```
## 处理属性的重要函数和属性
### 特殊属性
- __class__ 对象所属类的引用
- __dict__ 一个映射，存储对象和类的可写属性
- __slots__ 限制示例能够有哪些属性
### 内置函数
- dir([object]) 列出对象的大多数属性，无参会列出当前作用域的名称
- getattr(object,name[,default]) 从对象中获得name对应的属性
- hasattr(object,name) 判断存在与否
- setattr(object,name,value) 设定属性值
- vars([object]) 返回object的__dict__
### 特殊方法
- __delattr__(self,name) del删除属性时触发
- __dir__(self) 调用dir时触发
- __getattr__(self,name) 仅获取属性失败时
- __getattribute__(self,name) 当不是特殊属性和方法时，获取属性触发 ，抛出AttributeError调用__getattr__
- __setattr__(self,name,value) 设定属性值时调用


# Section14 属性描述符
创建一个实例，作为另一个类的类属性(注意哦创建是实例，作为另一个类的属性)

![设置托管属性](.\picture\设置托管属性.png)
![get&set](.\picture\get&set.png)
```
class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')
```
没有特别多想说的，一个更好的优化方案
```
import abc


class AutoStorage:  # 自动管理储存属性的描述符类
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)  # <2>


class Validated(abc.ABC, AutoStorage):  # 抽象类，覆盖__set__方法

    def __set__(self, instance, value):
        value = self.validate(instance, value)  # <4>
        super().__set__(instance, value)  # <5>

    @abc.abstractmethod
    def validate(self, instance, value):  # <6>
        """return validated value or raise ValueError"""


class Quantity(Validated):  # 实现非零的验证
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated): #实现非空字串验证
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value  # <8>
```
## 描述符类型
### 覆盖性描述符
因为实现__set__方法会覆盖实例属性的赋值操作，所以叫覆盖型描述符
而又由于存在__get__方法，常规读操作也会被描述符操作替代

这种方法，描述符会覆盖属性，无法用常规方法访问
### 没有__get__方法的覆盖性描述符
因为没有__get__，所以读操作会返回描述符本身

但这种方法，如果通过__dict__创建同名实例属性，因为没有__get__，读操作就会返回实例属性
### 非覆盖性描述符
若果有同名实例属性，那么描述符无法处理那个实例属性
### 但是呢
这一切都看的很美好，依附于类的描述符无法控制为类属性赋值的操作，

所以__set__无法控制对类属性的赋值操作！！！

若想控制设置类属性的操作，最好的方法就是将描述符依附于类的类上。
### 同时呢
这时候我们就来看下对于类和对象来说我们定义的方法有什么不同吧

obj.spam 绑定是是方法对象：可调用对象，里面包装着函数

Managed.spam 获取的是函数

所以函数体现出来其实就是个非覆盖性描述符
## 描述符用法
1. 使用特性以保持简单
内置property其实是覆盖性描述符，所以创建只读最好的方法就是用特性
2. 只读描述符必须要有__set__方法
为防止同名属性覆盖描述符，实现只读时，__get__、__set__都应该实现,__set__抛出AttributeError异常
3. 用于验证的描述符可以只有__set__方法
赋值验证最快捷的方法就是在__set__中检查，并最后在示例__dict__属性中设置
4. 仅有__get__方法的描述符可以实现高效缓存
这种方法用在get比较耗CPU时，之后可以用实例同名属性缓存结果
5. 非特殊方法可以被实例属性覆盖
因为特殊方法是基于x.__class__.__repr__(x)访问的，简单点说是类方法，所以不会被实例属性覆盖，但是非特殊方法__get__就会了。

# Section15 类元编程
## 类工厂函数
使用type构造类

```MyClass = type('MyClass',(MySuperClass,MyMixin),{'x':42,'x2':lambda self:self.x * 2})```

等同于
```
class MyClass(MySuperClass, MyMixin):
    x = 42

    def x2(self):
        return self.x * 2
```

```
def record_factory(cls_name,field_names):
    try:
        field_names = field_names.replace(',',' ').split()#贯彻鸭子类型，针对不同情况，最终实现结果
    except AttributeError:
        pass
    field_names = tuple(field_names)#使用属性名构建元组

    def __init__(self,*args,**kwargs):
        attrs = dict(zip(self.__slots__,args))
        attrs.update(kwargs)
        for name,value in attrs.items():
            setattr(self,name,value)
    
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self,name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__,self))
        return '{}({})'.format(self.__class__.__name__,values)

    cls_attrs = dict(__slots__ = field_names,#组建类的属性字典
                    __init__ = __init__,
                    __iter__ = __iter__,
                    __repr__ = __repr__)

    return type(cls_name,(object,),cls_attrs)#用type构造方法构造新类
```
神奇的type的实例是**类**
## 导入时和运行时
首先是编译的问题，不要把文件名命名为内部包名称，会导致文件编译后产生的.pyc文件影响其他文件导入内部包

其实是导包问题，会运行顶层代码

何为顶层代码：def语句、类的定义体构建类对象、

导入
```
>>> import evaltime
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha    #先运行装饰类定义体，再运行装饰器函数
<[9]> ClassFour body
<[14]> evaltime module end
```
运行
```
PS E:\py_work\fluent_python\Section15> python .\evaltime.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha
<[9]> ClassFour body
<[11]> ClassOne tests ..............................
<[3]> ClassOne.__init__
<[5]> ClassOne.method_x
<[12]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1 #被装饰器替代掉了方法
<[13]> ClassFour tests ..............................
<[10]> ClassFour.method_y #但是没有影响子类
<[14]> evaltime module end
<[4]> ClassOne.__del__ #结束后垃圾回收
```
## 元类
元类从type中获得了构建类的能力

[使用元类构建LineItem](.\picture\使用元类构建LineItem.png)

### __prepare__
知道类的属性构建的顺序

## 类作为对象
1. __mro__ 获取类的超类元组
2. __class__
3. __name__
4. __bases__ 由类的基类组成的元组
5. __qualname__ 从模块的全局作用域到类的点分路径
6. __subclasses__ 返回类的直接子类
