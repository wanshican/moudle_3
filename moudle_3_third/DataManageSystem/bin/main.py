import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import log_function, crawler, image, office, user_manage, decorate

def main():
    admin = user_manage.Admin()
    user = user_manage.User()
    if not os.path.exists(os.path.join(BASE_DIR, 'conf', 'user_info.ini')):
        admin.write_config()
    while True:
        print('欢迎使用数据管理系统，请先登录。')
        name = input('请输入用户名：')
        admin.config.read(admin.config_path)
        if name in admin.config.sections():
            if admin.config[name].get('type') == 'admin':
                info = admin.login(name)
                if info == 'sucess':
                    admin.show_menu()
                    print('4 : 开启权限')
                    print('5 : 关闭权限')
                else:
                    continue
            else:
                info = user.login(name)
                if info == 'sucess':
                    user.show_menu(name)
                else:
                    continue
        else:
            print('还未注册，是否注册？(y/n)。')
        select = input('请输入（n表示退出）：')
        if select == '1':
            url = input('请输入网址：')
            crawler.main(url)
        elif select == '2':
            name = input('请输入收件人姓名：')
            office.main(name)
        elif select == '3':
            sourse_dir = input('请输入图片文件目录：')
            image.main(sourse_dir)
        elif select == 'open':
            admin.open_authority()
        elif select == 'shut':
            admin.shut_authority()
        elif select == 'y':
            user.register()
        elif select == 'n':
            break
        else:
            break

def main2():
    admin = user_manage.Admin()
    user = user_manage.User()
    if not os.path.exists(os.path.join(BASE_DIR, 'conf', 'user_info.ini')):
        admin.write_config()
    while True:
        print('欢迎使用数据管理系统，请先登录。')
        name = input('请输入用户名：')
        admin.config.read(admin.config_path)
        if name not in admin.config.sections():
            print('还未注册，是否注册？(y/n)。')
        else:
            decorate.get_user_info(name)   # TODO 使用装饰器验证登录，验证成功后还需要输入一次密码，暂不知如何解决
            if admin.config[name].get('type') == 'admin':
                info = admin.login(name)
                if info == 'sucess':
                    admin.show_menu()
                else:
                    continue
            else:
                info = user.login(name)
                if info == 'sucess':
                    user.show_menu()
                else:
                    continue
        select = input('请输入（n表示退出）：')
        if select == '1':
            url = input('请输入网址：')
            crawler.main(url)
        elif select == '2':
            name = input('请输入收件人姓名：')
            office.main(name)
        elif select == '3':
            sourse_dir = input('请输入图片文件目录：')
            image.main(sourse_dir)
        elif select == 'y':
            user.register()
        elif select == 'n':
            break
        else:
            break

if __name__ == "__main__":
    main()