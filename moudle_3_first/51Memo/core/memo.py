import pickle
import os
import configparser

from . import log_function


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
        data = {'DEFAULT':{'base_dir':os.path.join(BASE_DIR, 'conf'),
                  'db_type':'pkl',
                  'name_pwd':os.path.join(BASE_DIR, 'db', 'name_pwd.pkl'),
                  'memo_list':os.path.join(BASE_DIR, 'db', 'memo_list.pkl')
                  }}
        for k,v in data.items():
            self.config[k] = v
            
        with open(self.config_path, 'w') as f:
            self.config.write(f)


    def load(self, name):
        '加载记录'
        self.config.read(self.config_path)
        if os.path.exists(os.path.join(BASE_DIR, 'db', f'{name}_memo.pkl')):
            with open(self.config[name].get('memo_list'), 'rb') as f:
                self.memo_list = pickle.loads(f.read())
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
        with open(os.path.join(BASE_DIR, 'db', f'{name}_name.pkl'), 'wb') as fw:
            fw.write(pickle.dumps(user))
            self.log.info('注册成功')
        self.config.read(self.config_path)
        self.config.add_section(name)
        self.add_config(name, 'name_pwd', os.path.join(BASE_DIR, 'db', f'{name}_name.pkl'))
        self.add_config(name, 'memo_list', os.path.join(BASE_DIR, 'db', f'{name}_memo.pkl'))


    def login(self):
        '登录'
        name = input('欢迎登录，请输入用户名：')
        pwd = input('请输入密码：')
        self.config.read(self.config_path)
        if name not in self.config.sections():
            self.log.info('还未注册，请先注册。')
        else:
            with open(self.config[name].get('name_pwd'), 'rb') as f:
                user_info = pickle.loads(f.read())
            if user_info['name'] == name and user_info['pwd'] == pwd:
                self.log.info('登录成功！')
                self.load(name)
                self.name = name
                return 'go_on'
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
        date = input('date:')
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
            self.log.info('查询到记录。')
            for k in self.memo_list:
                a = k['id']
                b = k['name']
                c = k['thing']
                d = k['date']
                print(f'记录{a}:{b} {c} {d}')
        else:
            print('暂无记录，请先添加。')
    

    def save(self): 
        '保存记录'
        with open(os.path.join(BASE_DIR, 'db', f'{self.name}_memo.pkl'), 'wb') as f:
            f.write(pickle.dumps(self.memo_list))
            self.log.info('保存成功')


def main():
    ma = MemoAdmin()
    if not os.path.exists(os.path.join(BASE_DIR, 'conf', 'memo.ini')):
        ma.write_config()
    print('欢迎使用51备忘录，请先登录。')
    while True:
        start = input('1：登录  2：注册  0：退出\n')
        if start == '1':
            info = ma.login()
            if info == 'go_on':
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
                    elif select == '0':
                        break
                    else:
                        break
        elif start == '2':
            ma.register()
        elif start == '0':
            break
        else:
            break

if __name__ == "__main__":
    main()
