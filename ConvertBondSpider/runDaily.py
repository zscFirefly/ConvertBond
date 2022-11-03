
from ScripyConvertBond import convertBondDaily
from scriptConfig import scriptConfig
from userLogin import *

if __name__ == '__main__':
    sc = scriptConfig() # 实例化配置对象

    us = userLogin(sc) # 实例化用户登陆对象
    login_info = us.get_login_info() # 获取登陆账号及登陆session
    us.activate(login_info) # 激活session
    sc.set_session(login_info['kbzw__Session']) # 更新配置对象cookies
    sc.set_user_login(login_info['kbzw__user_login']) # 更新配置对象cookies

    cb = convertBondDaily() # 初始化跑数实例
    cb.set_script_config(sc) # 设置配置项
    cb.run() # 跑数


