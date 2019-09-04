#字典推导
country_code = {country : code for code,country in [(1,'China'),(2,'EN')]}
print(country_code)
#setdefault
import sys,re
WORD_RE = re.compile(r'\w+')
index = {}
print(sys.argv[1])#运行时载入的参数
with open(sys.argv[1],encoding='utf-8') as fp:
    for line_no,line in enumerate(fp,1):
        #enumerate返回count和iterable参数返回的键值对
        for match in WORD_RE.finditer(line):
            #finditer返回MatchObject类型的iterable
            word = match.group()
            #返回匹配整体,用来提取分组截获的信息
            # print(match.start())
            column_no = match.start() + 1
            location = (line,column_no)
            index.setdefault(word,[]).append(location)

for key,text in index.items():
    print(key,text)

from collections import defaultdict,UserDict
dd = defaultdict(lambda : '<missing>')
print(dd[1])

#一个意外，StrKeyDict0的实现
class StrKeyDict0(dict): # 继承 dict
    def __missing__(self, key):
        if isinstance(key, str):
    # 如果找不到的键本身就是字符串，抛出 KeyError 
            raise KeyError(key)
    # 如果找不到的键不是字符串，转化为字符串再找一次
        return self[str(key)]
    def get(self, key, default=None):
    # get 方法把查找工作用 self[key] 的形式委托给 __getitem__，这样在宣布查找失败钱，还能通过 __missing__ 再给键一个机会
        try:
            return self[key]
        except KeyError:
    # 如果抛出 KeyError 说明 __missing__ 也失败了，于是返回 default 
            return default
    def __contains__(self, key):
    # 先按传入的键查找，如果没有再把键转为字符串再找一次
        return key in self.keys() or str(key) in self.keys()

class StrKeyDict(UserDict):
    def __missing__(self,key):
        if isinstance(key,str):
            raise KeyError(key)
        return self[str(key)]
    
    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item

