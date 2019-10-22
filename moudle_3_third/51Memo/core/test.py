from functools import wraps


class DecoAnything:
    def __init__(self, funcname, filename='log-test.txt'):
        self.filename = filename
        self.funcname = funcname
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kw):
            if hasattr(self, self.funcname):
                myfunc = getattr(self, self.funcname)
                if(myfunc(func)):
                    func(*args, **kw)
        return wrapper   

    def log(self, func):
        str_log = '函数{}开始运行...'.format(func.__name__)
        with open(self.filename, 'a', encoding='utf8') as f:
            print(str_log)
            f.write(str_log + '\n')
        return True

    def check(self, func):
        str_log = '函数{}开始运行...'.format(func.__name__)
        print(str_log)
        username = input('username: ')
        password = input('password: ')
        if username == 'de8ug' and password == '888':
            return True
        else:
            return False



