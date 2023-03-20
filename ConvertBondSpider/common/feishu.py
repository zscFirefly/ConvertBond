import sys
sys.path.append("..")
import pandas as pd 
import requests
import json


from conf.sql_config import *


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
     
        data = json.dumps(req_body) # 转化为str
        req = requests.post(url=url, data=data, headers=headers)
        print(req.json())
