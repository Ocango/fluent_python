import reprlib
import re

RE_WORD = re.compile('\w+')

class Sentence():
    def __init__(self,text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __getitem__(self,index):
        return self.words[index]
    
    def __len__(self):
        return len(self.words)
    
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

class Sentence_V1():
    def __init__(self,text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __iter__(self):
        #生成器函数
        for word in self.words:
            yield word
    def __len__(self):
        return len(self.words)
    
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

#惰性实现
class Sentence_V2():
    def __init__(self,text):
        self.text = text
    
    def __iter__(self):
        #生成器函数
        for match in RE_WORD.finditer(self.text):
            yield match.group()
        #生成器表达式
        # return (match.group() for match in RE_WORD.finditer(self.text))
    
    def __len__(self):
        return len(self.words)
    
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

