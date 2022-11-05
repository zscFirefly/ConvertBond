
from scripy_convert_bond import ConvertBondDaily
from script_config import ScriptConfig
from user_login import *
import datetime
from calender import Calender

if __name__ == '__main__':
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 判断是否为交易日，如果不为交易日，则不必执行
    ca = Calender(date)
    is_work = ca.get_is_work()
    if is_work == 0:
        print("今日%s，非交易日" % (date))
        exit()

    # 程序代码
    sc = ScriptConfig() # 实例化配置对象
    us = UserLogin(sc) # 实例化用户登陆对象

    login_info = us.login() # 登陆，获取登陆账号及登陆session
    us.activate_session(login_info) # 激活session
    sc.set_session(login_info['kbzw__Session']) # 更新配置对象的cookies值
    sc.set_user_login(login_info['kbzw__user_login']) # 更新配置对象的cookies值

    cb = ConvertBondDaily() # 初始化跑数实例
    cb.set_script_config(sc) # 设置配置项
    cb.run() # 跑数


