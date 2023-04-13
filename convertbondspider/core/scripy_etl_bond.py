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
from core.script_etl_config import * 
from core.script_etl_config import ScriptETLConfig
from core.user_login import *
from common.calender import Calender

class ScriptETL():
    def __init__(self):
        self.script_etl_config = None

    def set_script_etl_config(self,script_etl_config):
        self.script_etl_config = script_etl_config

    def util_to_df(self,debt_json):
        ## 将获取下来的数据由json转化为dataframe
        finish_data = pd.DataFrame()
        # print(debt_json)
        for debt in debt_json:
            debt['etf_types'] = str(debt['etf_types'])

            finish_data = pd.concat([finish_data,pd.DataFrame(debt,index=[1])],axis=0)

            # tmp_data = pd.DataFrame(debt,index=[0]) # 爬code的时候，记得修改
            # tmp_data = pd.DataFrame(debt['cell'],index=[0])
            # finish_data = finish_data.append(tmp_data,ignore_index=True)
        return finish_data

    def get_etl_code(self):
        url = 'https://stock.xueqiu.com/v5/stock/screener/fund/list.json'
        data = {
            'type': '18',
            'parent_type': '1',
            'order': 'desc',
            'order_by': 'percent',
            'page': '1',
            'size': '1000',
        }

        response = requests.get(url = url,params=data,cookies=self.script_etl_config.get_cookies(),headers=self.script_etl_config.get_headers())
        etl_list = response.json()['data']['list']
        df = self.util_to_df(etl_list)
        return df

    def change_timestamp2date(self,ts_ms):
        ts_sec = ts_ms / 1000  # 转换为秒
        utc_datetime = datetime.datetime.utcfromtimestamp(ts_sec)  # 转换为UTC时间
        local_datetime = utc_datetime + datetime.timedelta(hours=8)  # 转换为当地时间（北京时间）
        date_str = local_datetime.strftime('%Y-%m-%d')  # 转换为%Y-%m-%d格式的字符串
        return date_str

    def run(self):
        table_name = 'dev_etl_bond_info'
        df = self.get_etl_code()
        print(df.columns)
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



if __name__ == '__main__':
    sc = ScriptETLConfig() # 实例化配置对象
    se = ScriptETL()
    se.set_script_etl_config(sc)
    df = se.run()
    # print(df)
