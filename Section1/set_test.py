#集合推导
from unicodedata import name
a = {
    chr(i) for i in range(32,256) if 'SIGN' in name(chr(i),'')
}
print(a)
