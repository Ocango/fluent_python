# s = 'ac✂12‰'

# print(len(s))
# #编码
# a = s.encode('utf-8')
# print(a)
# #解码
# b = a.decode('utf-8')
# print(b)
# #定义bytes变量
# cafe = bytes('ac✂12‰',encoding = 'utf-8')
# print(cafe)
# print(cafe[2])
# print(cafe[:3])
# cafe_arr = bytearray(cafe)
# print(cafe_arr[1:])
# #解析十六进制
# print(bytes.fromhex('B901EF'))
import struct
fmt = '<3s3sHH'
with open('desktop.jpg','rb') as fq:
    img = memoryview(fq.read())#使用内存中的文件内容创建memeryview对象
header = img[:10]
print(bytes(header))
print(struct.unpack(fmt,header))#拆包memoryview对象
del header
del img

# from unicodedata import normalize
# '''
# NFC     最小码位都成等价字符
# NFD     拆解成基字符的组合字符
# 这两个会把兼容字符分解成兼容分解字符，
# 会曲解原意但有利于将单字符解析成有意义的多字符
# NFKC    
# NFKD
# '''

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
    