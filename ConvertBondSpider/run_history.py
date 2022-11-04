from scripy_convert_bond import ConvertBondHistory
from script_config import ScriptConfig
from user_login import *


if __name__ == '__main__':
    # cb = convertBondHistory()
    # cb.run()


    sc = ScriptConfig() # 实例化配置对象

    us = UserLogin(sc) # 实例化用户登陆对象
    login_info = us.login() # 获取登陆账号及登陆session
    us.activate_session(login_info) # 激活session
    sc.set_session(login_info['kbzw__Session']) # 更新配置对象cookies
    sc.set_user_login(login_info['kbzw__user_login']) # 更新配置对象cookies

    cb = ConvertBondHistory() # 初始化跑数实例
    cb.set_script_config(sc) # 设置配置项
    cb.run() # 跑数