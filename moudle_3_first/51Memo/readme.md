# 51Memo
# Author: wanshican


# 针对上次作业的 Memo Admin类
1. 添加注册和登陆功能，用户名密码使用dict保存为: users. pkl
2. 添加配置文件，为备忘录数据指定路径类型和文件名。比如 zhangsan，则效据文件可以为 zhangsan.pkl或 zhangsan.db。
3. 注册时，相应数据文件根据用户名在配置文件保存为新的 secton。比如 zhangsan，则有新的 section!叫[zhangsan]
4. 启动程序先提示登陆，每次登陆时候，先根据配置文件读取用户信息，找不到则提示注册。
5. 导出文件功能，将历史数据导出为pdf文件
6. 对每一个函数操作添加日志功能，并在需要时候随时关闭。