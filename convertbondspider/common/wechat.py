import sys
sys.path.append("..")
import pandas as pd 
import requests
import json



from conf.wechat_config import *


class WeChat():
    '''监控类'''
    def __init__(self,config):
        self.config = config
        self.user = ""
        self.party = ""
        self.tag = ""

    def set_user(self,user):
        self.user = user

    def set_party(self,party):
        self.party = party

    def set_tag(self,tag):
        self.tag = tag

    def set_agentid(self,agentid):
        self.agentid = agentid



    def get_access_token(self):


        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (self.config.corpid,self.config.corpsecret)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',        
        }
        res= requests.post(url, headers=headers)
        return res.json()['access_token']


    def send_message(self, text):
        access_token = self.get_access_token()

        data = {
            "touser": self.user,
            "toparty": self.party,
            "totag": self.tag,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {"content": text},
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0
        }
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?debug=1&access_token=%s" % (access_token)

        res = requests.post(url=url, json=data)
        print(res.json())

if __name__ == '__main__':
    wcc = WeChatConfig()
    wcc.set_corpid('wwf61f5f63b0d60a9a')
    wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')
    wc = WeChat(wcc)
    wc.set_user("ZhengShuoCong")
    wc.set_agentid(1000002)
    wc.send_message("hello world")

