import sys
sys.path.append("..")
import json
import requests
import pandas as pd 
import datetime

from conf.sql_config import *
from conf.feishu_config import *
from common.search_data import SearchData
from common.feishu import FeiShu



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

    fs = FeiShu(fc)
    fs.send_message(message)


