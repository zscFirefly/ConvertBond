import requests
from scriptConfig import scriptConfig


class userLogin():
    def __init__(self,scriptConfig):
        self.scriptConfig = scriptConfig

    def get_login_info(self):

        data = {
            'return_url': 'https://www.jisilu.cn/',
            'user_name': '82285207dcc05a2e0d18d0831876a016',
            'password': 'd071ff68bdd0e7af7941c90d3440c1e5',
        }
        url = 'https://www.jisilu.cn/webapi/account/login_process/'

        response = requests.post(url=url, headers=self.scriptConfig.get_headers(), data=data)

        login_info = response.cookies.get_dict()
        print("login in info ==> " + str(login_info))

        return login_info


    def activate(self,login_info):
        url = 'https://www.jisilu.cn/'
        response = requests.get(url=url, cookies=login_info, headers=self.scriptConfig.get_headers())
        print("activate status ==> " + str(response.status_code))


if __name__ == '__main__':
    sc = scriptConfig()
    us = userLogin(sc)
    login_info = us.get_login_info()
    us.activate(login_info)
    sc.set_session(login_info['kbzw__Session'])
    sc.set_user_login(login_info['kbzw__user_login'])
    print(sc.get_cookies())

    