import json
import requests
import pandas as pd 
from sql_config import *
import datetime

class FeishuConfig():
    '''飞书配置类'''
    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.user_id = None
        self.union_id = None
        self.open_id = None

    def set_app_id(self,app_id):
        self.app_id = app_id

    def set_app_secret(self,app_secret):
        self.app_secret = app_secret

    def set_user_id(self,user_id):
        self.user_id = user_id

    def set_union_id(self,union_id):
        self.union_id = union_id

    def set_open_id(self,open_id):
        self.open_id = open_id


class SearchData():
    '''sql查询类'''
    def __init__(self,sql):
        self.sql = sql

    def read_data(self):
        data = pd.read_sql(self.sql, sqlExecute.engine)
        return data


class Monitor():
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

 




if __name__ == '__main__':
    # app_id = 'cli_a3ee5eca19b9900d'
    # app_secret = 'sSjQawQabi0sdODSiCxoggeMLhNEWnq7'
    # user_id = '41a6a2ba'
    # union_id = 'on_ae6473e89d04c5512829141d428ff083'
    # open_id = 'ou_55a5f41a397faced09f3ed94eace29f5'
    print("开始执行：%s" % (datetime.datetime.now()))

    message = '%s可转债数据：\n双低均值：%s\n价格均值：%s\n溢价率均值：%s'
    sql = '''
    select round(avg(price),2) as avg_price
    ,round(avg(premium_rt),2) as avg_premium_rt
    ,round(avg(price+premium_rt),2) as avg_double
    from convert_bond_daily
    where date = CURRENT_DATE
    and price <> 100 and increase_rt <>0
    '''

    sd = SearchData(sql)
    df = sd.read_data()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    message = message % (date, df.at[0,'avg_price'], df.at[0,'avg_premium_rt'], df.at[0,'avg_double'])
    

    fc = FeishuConfig()
    fc.set_user_id('41a6a2ba')
    fc.set_app_id('cli_a3ee5eca19b9900d')
    fc.set_app_secret('sSjQawQabi0sdODSiCxoggeMLhNEWnq7')

    mo = Monitor(fc)
    mo.send_message(message)


