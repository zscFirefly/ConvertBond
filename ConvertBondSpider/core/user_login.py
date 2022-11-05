import sys
sys.path.append("..")
import requests

from core.script_config import ScriptConfig



class UserLogin():
    def __init__(self,script_config):
        self.script_config = script_config

    def login(self):

        data = {
            'return_url': 'https://www.jisilu.cn/',
            'user_name': '82285207dcc05a2e0d18d0831876a016',
            'password': 'd071ff68bdd0e7af7941c90d3440c1e5',
        }
        url = 'https://www.jisilu.cn/webapi/account/login_process/'

        response = requests.post(url=url, headers=self.script_config.get_headers(), data=data)

        login_info = response.cookies.get_dict()
        print("login in info ==> " + str(login_info))

        return login_info


    def activate_session(self,login_info):
        url = 'https://www.jisilu.cn/'
        response = requests.get(url=url, cookies=login_info, headers=self.script_config.get_headers())
        print("activate status ==> " + str(response.status_code))


if __name__ == '__main__':
    sc = ScriptConfig()
    us = UserLogin(sc)
    login_info = us.login()
    us.activate_session(login_info)
    sc.set_session(login_info['kbzw__Session'])
    sc.set_user_login(login_info['kbzw__user_login'])
    print(sc.get_cookies())

    