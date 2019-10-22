import pickle
import os
import configparser
import datetime
import json
from dateutil import parser
from functools import wraps

import log_function

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Admin:
    """管理员"""
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(BASE_DIR, 'conf', 'user_info.ini')
        self.log = log_function.use_log(log_file=os.path.join(BASE_DIR, 'log', 'data_manage.log'))
    
    def write_config(self):
        '初始化配置文件'
        data = {'DEFAULT':{
                        'base_dir':os.path.join(BASE_DIR, 'conf'),
                        'type':'user',
                        'operation':[],
                        'name_pwd':os.path.join(BASE_DIR, 'db', 'name_pwd.json')
                  },
                  'admin':{
                      'base_dir':os.path.join(BASE_DIR, 'conf'),
                      'type':'admin',
                      'operation':os.path.join(BASE_DIR, 'db', 'operation.json'),
                      'name_pwd':os.path.join(BASE_DIR, 'db', 'admin.json')
                  }}
        for k,v in data.items():
            self.config[k] = v

        with open(self.config_path, 'w') as f:
            self.config.write(f)

        with open(os.path.join(BASE_DIR, 'db', 'admin.json'), 'w') as fw:
            json.dump({'name':'admin', 'pwd':'admin'}, fw)

        with open(os.path.join(BASE_DIR, 'db', 'operation.json'), 'w') as fw:
            json.dump(['crawler', 'office', 'image'], fw)

    def login(self, name):
        self.config.read(self.config_path)
        pwd = input('请输入密码：')
        with open(self.config[name].get('name_pwd'), 'r') as f:
            user_info = json.load(f)
        if user_info['name'] == name and user_info['pwd'] == pwd:
            self.log.info('登录成功！')
        else:
            self.log.warning('用户名或密码错误，请重试！')

    def show_menu(self):
        with open(os.path.join(BASE_DIR, 'db', 'operation.json'), 'r') as f:
            menu = json.load(f)
            for i, m in enumerate(menu):
                print(i+1, ':', m)



class User:
    """管理员"""
    def __init__(self):
        self.name = None
        self.memo_list = []
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(BASE_DIR, 'conf', 'user_info.ini')
        self.log = log_function.use_log(log_file=os.path.join(BASE_DIR, 'log', 'data_manage.log'))
   
    def add_config(self, section, option, value):
        '新增配置文件'
        try:
            self.config.read(self.config_path)
            self.config.set(section, option, value)
            with open(self.config_path, 'w') as f:
                self.config.write(f)
        except Exception as e:
            print(e)

    def register(self):
        '注册'
        name = input('请输入注册用户名：')
        pwd = input('请输入注册密码：')
        user = {'name': name, 'pwd': pwd}
        with open(os.path.join(BASE_DIR, 'db', f'{name}.json'), 'w') as fw:
            json.dump(user, fw)
            self.log.info('注册成功')
        self.config.read(self.config_path)
        self.config.add_section(name)
        self.add_config(name, 'name_pwd', os.path.join(BASE_DIR, 'db', f'{name}.json'))

    def login(self, name):
        pwd = input('请输入密码：')
        self.config.read(self.config_path)
        with open(self.config[name].get('name_pwd'), 'r') as f:
            user_info = json.load(f)
        if user_info['name'] == name and user_info['pwd'] == pwd:
            self.log.info('登录成功！')
        else:
            self.log.warning('用户名或密码错误，请重试！')

    def show_menu(self):
        menu = []
        for i, m in enumerate(menu):
            print(i+1, ':', m)

def main():
    admin = Admin()
    user = User()
    if not os.path.exists(os.path.join(BASE_DIR, 'conf', 'admin.ini')):
        admin.write_config()
    print('欢迎使用数据管理系统，请先登录。')
    name = input('请输入用户名：')
    admin.config.read(admin.config_path)
    if name in admin.config.sections():
        if admin.config[name].get('type') == 'admin':
            admin.login(name)
            admin.show_menu()
        else:
            user.login(name)
            user.show_menu()
    else:
        admin.log.info('还未注册，请先注册。')
        user.register()


if __name__ == "__main__":
    main()
