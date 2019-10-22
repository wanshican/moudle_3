import pickle
import os
import configparser
import datetime
import json
from dateutil import parser
from functools import wraps
import smtplib
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import log_function


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Memo:
    def __init__(self,name,thing,date):
        '初始化数据'
        self.name = name
        self.thing = thing
        self.date = date
    

class MemoAdmin:
    """管理记录"""
    def __init__(self):
        self.name = None
        self.memo_list = []
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(BASE_DIR, 'conf', 'memo.ini')
        self.log = log_function.use_log(log_file=os.path.join(BASE_DIR, 'log', 'memo.log'))
    
    def write_config(self):
        '初始化配置文件'
        data = {'DEFAULT':{
                        'base_dir':os.path.join(BASE_DIR, 'conf'),
                        'type':'user',
                        'operation':[],
                        'name_pwd':os.path.join(BASE_DIR, 'db', 'name_pwd.json'),
                        'memo_list':os.path.join(BASE_DIR, 'db', 'memo_list.json')
                  },
                  'admin':{
                      'base_dir':os.path.join(BASE_DIR, 'conf'),
                      'type':'admin',
                      'operation':os.path.join(BASE_DIR, 'db', 'operation.json'),
                      'name_pwd':os.path.join(BASE_DIR, 'db', 'admin.json'),
                      'memo_list':os.path.join(BASE_DIR, 'db', 'admin_memo.json')
                  }}
        for k,v in data.items():
            self.config[k] = v

        with open(self.config_path, 'w') as f:
            self.config.write(f)

        with open(os.path.join(BASE_DIR, 'db', 'admin.json'), 'w') as fw:
            json.dump({'name':'admin', 'pwd':'admin'}, fw)

        with open(os.path.join(BASE_DIR, 'db', 'operation.json'), 'w') as fw:
            json.dump(['login', 'register', 'memo_operate', 'crawler', 'office', 'image'], fw)
   
    def load(self, username):
        '加载记录'
        self.config.read(self.config_path)
        if os.path.exists(os.path.join(BASE_DIR, 'db', f'{username}_memo.json')):
            with open(self.config[username].get('memo_list'), 'r') as f:
                self.memo_list = json.load(f)
                self.query()
                self.log.info('加载成功')

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
        self.add_config(name, 'memo_list', os.path.join(BASE_DIR, 'db', f'{name}_memo.json'))

    def login(self):
        name = input('请输入用户名：')
        pwd = input('请输入密码：')
        self.name = name
        self.config.read(self.config_path)
        if name not in self.config.sections():
            self.log.info('还未注册，请先注册。')
        else:
            with open(self.config[name].get('name_pwd'), 'r') as f:
                user_info = json.load(f)
            if user_info['name'] == name and user_info['pwd'] == pwd:
                self.log.info('登录成功！')
                self.load(name)
            else:
                self.log.warning('用户名或密码错误，请重试！')

    def export_pdf(self):
        '导出pdf文件'
        with open(os.path.join(BASE_DIR, 'db', 'memo.pdf'), 'w') as f:
            for item in self.memo_list:
                f.write(str(item['id']) + ' ' + item['name'] + ' ' + item['thing'] + ' ' + item['date'] + '\n')
        self.log.info('导出成功！')

    def welcome(self):
        '打印选择菜单'
        dir = {'1':'Add',
                '2':'Dele',
                '3':'Modify',
                '4':'Query',
                '5':'Save',
                '6':'export_pdf',
                '7':'返回查询数据',
                '8':'发送数据到邮箱',
                '0':'退出'
                }
        print('欢迎使用51备忘录'.center(50, '-'))
        for k,v in dir.items():
            print(f'{k}:{v}')        
        select = input('请选择你的操作选项 (示例 1)：')
        return select

    def get_id(self):
        if self.memo_list:
            i = 1
            for item in self.memo_list:
                item['id'] = i
                i += 1
        else:
            print('暂无记录，请先添加。')

    def add(self): 
        '新增记录'
        name = input('name:')
        thing = input('thing:')
        date = input('date:(示例：1.1)')
        month, day = date.split('.')
        now = datetime.datetime.now()
        new_time = now.replace(day=int(day), month=int(month))
        date = new_time.strftime(f'%Y-%m-%d %X')
        memo = Memo(name, thing, date)
        one = {'name': memo.name, 'thing': memo.thing, 'date': memo.date}
        self.memo_list.append(one)
        self.get_id()
        self.log.info('增加成功')
      
    def dele(self):
        '删除记录'
        try:
            num = input('请选择你将要删除的记录（示例 1或者2或者3 ）:')
            self.memo_list.pop(int(num)-1)
            self.get_id()
            self.log.warning('成功删除记录。')
        except IndexError as e:
            print('抱歉，找不到记录，请重试', e)
    
    def modify(self):
        '修改记录'
        try:
            num = input('请输入你要修改的记录（示例 1或者2或者3）:')
            text = input(f'你要修改的记录是{self.memo_list[int(num)-1]}，请输入要修改的值（示例：name:张三）:')
            new_text = text.split(':')
            self.memo_list[int(num)-1][new_text[0]] = new_text[1]
            self.log.info('修改成功')
        except IndexError as e:
            print('抱歉，找不到记录，请重试', e)
    
    def query(self): 
        '查询记录'
        if self.memo_list:
            self.log.info(f'查询到{len(self.memo_list)}条记录。')
            for k in self.memo_list:
                a = k['id']
                b = k['name']
                c = k['thing']
                d = k['date']
                print(f'记录{a}:{b} {c} {d}')
        else:
            print('暂无记录，请先添加。')
    
    def query_memo(self):
        ret = {'status': 0, 'statusText': '查询成功！', 'data':[]}
        from_month = int(input('请输入起始月份：'))
        to_month = int(input('请输入截止月份:'))
        try:
            for item in self.memo_list:
                month = parser.parse(item['date']).month
                if month >= from_month and month <= to_month:
                    ret['data'].append(item)
            if ret['data']:
                self.log.info('成功返回json数据')
            elif not ret['data']:
                self.log.error('没有符合要求的记录！')
                return
        except Exception as e:
            ret['status'] = 1
            ret['statusText'] = e
        return ret

    def send_email(self):
        smtp = SMTP_SSL("smtp.qq.com")
        smtp.ehlo("smtp.qq.com")
        smtp.login("1483204124@qq.com", '')
        select_data = []
        info = input('请输入月份或年份：')
        if info.endswith('年') or info.endswith('月'):
            if len(info.strip('年').strip('月')) > 2:
                for item in self.memo_list:
                    year = parser.parse(item['date']).year
                    if year == int(info.strip('年').strip('月')):
                        select_data.append(item)
            else:
                for item in self.memo_list:
                    month = parser.parse(item['date']).month
                    if month == int(info.strip('年').strip('月')):
                        select_data.append(item)
            if select_data:
                text = ''
                for item in select_data:
                    memo_data = str(item['id']) + ' ' + str(item['name']) + ' ' + str(item['thing']) + ' ' + str(item['date']) + '\n'
                    text += memo_data
                msg = MIMEText(text, "plain", "utf-8")
                msg["Subject"] = Header("邮件标题", "utf-8")
                msg["from"] = "1483204124@qq.com"
                msg["to"] = "wanshican@163.com"
                smtp.sendmail("1483204124@qq.com", "wanshican@163.com", msg.as_string())
                smtp.quit()
                self.log.info('数据发送成功!')
            else:
                self.log.error('未查询到符合要求的数据！')
        else:
            self.log.error('请输入正确的查询条件！')

    def save(self): 
        '保存记录'
        with open(os.path.join(BASE_DIR, 'db', f'{self.name}_memo.json'), 'w') as f:
            json.dump(self.memo_list, f)
            self.log.info('保存成功')

    def show_menu(self):
        try:
            self.config.read(self.config_path)
            if self.name not in self.config.sections():
                menu = ['login', 'register']
                for i, m in enumerate(menu):
                    print(i+1, ':', m)
            elif self.config[self.name].get('type') == 'admin':
                with open(os.path.join(BASE_DIR, 'db', 'operation.json'), 'r') as f:
                    menu = json.load(f)
                    for i, m in enumerate(menu):
                        print(i+1, ':', m)
            elif self.config[self.name].get('type') == 'user':
                menu = ['memo_operate']
                for i, m in enumerate(menu):
                    print(i+3, ':', m)
        except Exception as e:
            print(e)


def main():
    ma = MemoAdmin()
    if not os.path.exists(os.path.join(BASE_DIR, 'conf', 'memo.ini')):
        ma.write_config()
    print('欢迎使用51备忘录，请先登录。')
    ma.login()
    while True:
        ma.show_menu()
        start = input('请选择序号（0表示退出）：')
        if start == '3':
            while True:
                select = ma.welcome()
                if select == '1':
                    ma.add()
                elif select == '2':
                    ma.dele()    
                elif select == '3':
                    ma.modify()
                elif select == '4':
                    ma.query()
                elif select == '5':
                    ma.save()
                elif select == '6':
                    ma.export_pdf()
                elif select == '7':
                    ma.query_memo()
                elif select == '8':
                    ma.send_email()
                elif select == '0':
                    break
                else:
                    break
        elif start == '1':
            ma.login()
        elif start == '2':
            ma.register()
        elif start == '4':
            print('开发中...')
        elif start == '5':
            print('开发中...')
        elif start == '6':
            print('开发中...')
        elif start == '0':
            break
        else:
            break

if __name__ == "__main__":
    main()
