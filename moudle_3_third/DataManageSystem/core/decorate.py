#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# 装饰器,案例，验证登陆状态
# author: wanshican

import os
import json
import configparser
from functools import wraps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config_path = os.path.join(BASE_DIR, 'conf', 'user_info.ini')

class DecoAnything:
    def __init__(self, funcname):
        self.funcname = funcname
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kw):
            if hasattr(self, self.funcname):
                myfunc = getattr(self, self.funcname)
                if(myfunc(*args, func=func)):
                    func(*args, **kw)
        return wrapper   

    def check(self, *args, func):
        username = args[0]
        password = input('请输入密码: ')
        return auth(username, password)


def auth(username, password):
    """判断密码是否正确
    """
    if password == get_password(username):  # 读取数据，返回密码
        print('登录成功！')
        return True
    else:
        print('密码错误，请重试！')
        return False
        
def get_password(username):
    '''根据用户名，获取密码'''
    config.read(config_path)
    with open(config[username].get('name_pwd'), 'r') as f:
        user_info = json.load(f)
    return user_info['pwd']

    

@DecoAnything('check')
def get_user_info(username):
    print(f'嗨，你好呀，{username}')


def main(name='wanshican'):
    name = input('用户名：')
    get_user_info(name)


if __name__ == '__main__':
    main()