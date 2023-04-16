#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:01:52 2023

@author: zhengshuocong
"""

import sys
sys.path.append("..")
import requests
import pandas as pd
import datetime
import time

from conf.sql_config import *
from core.script_etf_config import * 
from core.script_etf_config import ScriptetfConfig
from core.user_login import *
from common.calender import Calender

class ScriptETF():
    def __init__(self):
        self.script_etf_config = None

    def set_script_etf_config(self,script_etf_config):
        self.script_etf_config = script_etf_config

    def util_to_df(self,debt_json):
        ## 将获取下来的数据由json转化为dataframe
        finish_data = pd.DataFrame()
        # print(debt_json)
        for debt in debt_json:
            debt['etf_types'] = str(debt['etf_types'])
            finish_data = pd.concat([finish_data,pd.DataFrame(debt,index=[1])],axis=0)

        return finish_data

    def get_etf_code(self):
        url = 'https://stock.xueqiu.com/v5/stock/screener/fund/list.json'
        data = {
            'type': '18',
            'parent_type': '1',
            'order': 'desc',
            'order_by': 'percent',
            'page': '1',
            'size': '1000',
        }

        response = requests.get(url = url,params=data,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        etf_list = response.json()['data']['list']
        df = self.util_to_df(etf_list)
        return df


    def get_etf_info(self):
        url = 'https://stock.xueqiu.com/v5/stock/screener/fund/list.json'
        data = {
            'type': '18',
            'parent_type': '1',
            'order': 'desc',
            'order_by': 'percent',
            'page': '1',
            'size': '1000',
        }

        response = requests.get(url = url,params=data,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        etf_list = response.json()['data']['list']
        df = self.util_to_df(etf_list)
        return df


    def get_etf_detail(self,code):
        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?"
        data = {
            'symbol': code, 
            'begin': str(int(time.time() * 1000)), 
            'period': 'day', 
            'type': 'before', 
            'count': '-4000', 
            'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance,macd'
        } 

        response = requests.get(url = url,params=data,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        res_column = response.json()['data']['column']
        res_items = response.json()['data']['item']
        json_list = []
        df = pd.DataFrame()
        for item in res_items:
            zipped= dict(zip(res_column,item))
            df = pd.concat([df,pd.DataFrame(zipped,index=[1])],axis=0)
        return df


    def change_timestamp2date(self,ts_ms):
        ts_sec = ts_ms / 1000  # 转换为秒
        utc_datetime = datetime.datetime.utcfromtimestamp(ts_sec)  # 转换为UTC时间
        local_datetime = utc_datetime + datetime.timedelta(hours=8)  # 转换为当地时间（北京时间）
        date_str = local_datetime.strftime('%Y-%m-%d')  # 转换为%Y-%m-%d格式的字符串
        return date_str


    def read_etf_code(self):
        # data = pd.read_csv('debt_code.csv')
        today = datetime.date.today()
        sql = '''select symbol from dev_etf_fund_info  where timestamp = '%s' ;''' % (today)
        data = pd.read_sql(sql=sql, con=sqlExecute.engine)
        return data

    def run(self):
        table_name = 'dev_etf_fund_detail'
        df = self.get_etf_code()
        # print(df.columns)
        df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
        ts_list = df['timestamp'].drop_duplicates()
        if len(ts_list) >= 2:
            print("Error: 所爬数据出现跨日期异常！")
            print(ts_list)
            exit();

        print("开始删除数据.....")
        sql = "delete from %s where `timestamp` = '%s' " % (table_name,ts_list[1])
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        print("删除数据完成。")        

        df.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        # df = self.get_etf_detail('SH516510')
        # print(df)
        # table_name = 'dev_etf_fund_detail'
        df = self.read_etf_code()
        etf_codes = df['symbol'].tolist()
        for etf_code in etf_codes:
            df = self.get_etf_detail(etf_code)
            df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
            df['symbol'] = etf_code
            df.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
            print("获取etf：%s" %(etf_code) )
            time.sleep(0.5)







if __name__ == '__main__':
    sc = ScriptetfConfig() # 实例化配置对象
    se = Scriptetf()
    se.set_script_etf_config(sc)
    df = se.run()
    # print(df)
