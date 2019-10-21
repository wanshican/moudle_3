#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# 装饰器,各种用途
# author: De8uG


from functools import wraps


class DecoLog:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kw):
            str_log = '函数{}开始运行...'.format(func.__name__)
            with open(self.filename, 'a', encoding='utf8') as f:
                print(str_log)
                f.write(str_log + '\n')
            func(*args, **kw)
        return wrapper


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


# @DecoLog('log.txt')
@DecoAnything('log')
@DecoAnything('check')
def tony():
    print('我是tony在函数', tony.__name__)


def main():
    tony()

if __name__ == '__main__':
    main()