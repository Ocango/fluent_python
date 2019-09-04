class LookingGlass():
    def __enter__(self):
        import sys 
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'
    
    def reverse_write(self,text):
        self.original_write(text[::-1])
    
    def __exit__(self,exc_type,exc_value,traceback):#exc_type异常类，exc_value.args异常实例，有些参数传给异常构造方法，traceback对象，在finally中调用sys.exe_info()得到的就是这三个参数
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero')
            return True
    
