import sys
sys.path.append("..")
import pandas as pd 
import requests
import json


from conf.sql_config import *

from core.monitor import *
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig

class FeiShu():
    '''监控类'''
    def __init__(self,config):
        self.config = config

    def get_tenant_access_token(self):
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        data = {
            'app_id': self.config.app_id,
            'app_secret': self.config.app_secret
        }

        headers = {
            'Content-Type': 'application/json; charset=utf-8',        
        }
        res= requests.post(url, params=data, headers=headers).json() 
        print(res) 
        return res['tenant_access_token']


    def send_message(self, text):
        url = "https://open.feishu.cn/open-apis/message/v4/send/"     
        access_token = self.get_tenant_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }
        req_body = {
            "user_id": self.config.user_id,
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        print(self.config.user_id)
     
        data = json.dumps(req_body) # 转化为str
        req = requests.post(url=url, data=data, headers=headers)
        print(req.json())


if __name__ == '__main__':
    # main()


    fc = FeishuConfig()
    fc.set_user_id('41a6a2ba')
    fc.set_app_id('cli_a3ee5eca19b9900d')
    fc.set_app_secret('sSjQawQabi0sdODSiCxoggeMLhNEWnq7')

    # 构造飞书-监控实例
    fs = FeiShu(fc)
    fs.send_message("hello world") # 发送消息