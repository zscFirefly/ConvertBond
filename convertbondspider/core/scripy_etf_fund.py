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
import talib
import numpy as np
pd.set_option('expand_frame_repr', False)

from conf.sql_config import *
from core.script_etf_config import * 
from core.script_etf_config import ScriptETFConfig
from core.user_login import *
from common.calender import Calender
from datetime import datetime, timedelta


class ScriptETF():
    def __init__(self):
        self.script_etf_config = None
        self.etf_info_table_name = 'dev_etf_fund_info'
        self.etf_detail_table_name = 'dev_etf_fund_detail'
        self.etf_macd_table_name = 'dev_etf_macd_data'

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
        utc_datetime = datetime.utcfromtimestamp(ts_sec)  # 转换为UTC时间
        local_datetime = utc_datetime + datetime.timedelta(hours=8)  # 转换为当地时间（北京时间）
        date_str = local_datetime.strftime('%Y-%m-%d')  # 转换为%Y-%m-%d格式的字符串
        return date_str


    def read_etf_code(self):
        # data = pd.read_csv('debt_code.csv')
        # today = datetime.date.today()
        today = '2023-04-14'
        sql = '''select symbol from dev_etf_fund_info  where timestamp = '%s' ;''' % (today)
        print(sql)
        data = pd.read_sql(sql=sql, con=sqlExecute.engine)
        return data


    def subtract_one_day(date_str,i):
        # 将字符串形式的日期转换为datetime对象
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # 减去一天
        new_date_obj = date_obj - timedelta(days=i)
        # 将结果转换回字符串形式
        new_date_str = new_date_obj.strftime('%Y-%m-%d')
        
        return new_date_str


    def get_condition_date(self,date):
        get_date_sql = 'select timestamp from dev_etf_macd_data where timestamp <= "%s" group by timestamp order by timestamp desc' % (date)
        date_df = pd.read_sql(sql=get_date_sql, con=sqlExecute.engine)
        

        ## 比如：我需要获取03-01的数据，那么，我需要去拿相应日期前几天的macd值
        sql = ''' select * from (
            select symbol
            , sum(case when timestamp = '{6}' then macd else null end) as a
            , sum(case when timestamp = '{5}' then macd else null end) as b
            , sum(case when timestamp = '{4}' then macd else null end) as c
            , sum(case when timestamp = '{3}' then macd else null end) as d
            , sum(case when timestamp = '{2}' then macd else null end) as e
            , sum(case when timestamp = '{1}' then macd else null end) as f
            , sum(case when timestamp = '{0}' then macd else null end) as g
            , sum(case when timestamp = '{0}' then close else null end) as close
            , sum(case when timestamp = '{0}' then amount else null end) as amount
            from {table_name} where timestamp >= '{6}' 
            group by symbol
        )a 
        where a < b
        and b < c
        and c < d
        and d < e
        and e < f
        and f < g
        and a < 0
        and b < 0
        and c < 0
        and g > 0
        and amount > 100000000
        and close < 10
        '''.format(date_df.at[0,'timestamp'],date_df.at[1,'timestamp'],date_df.at[2,'timestamp'],date_df.at[3,'timestamp'],date_df.at[4,'timestamp'],date_df.at[5,'timestamp'],date_df.at[6,'timestamp'],table_name = self.etf_macd_table_name)
        print(sql)
        df = pd.read_sql(sql=sql, con=sqlExecute.engine)
        print(df)




    def get_condition_fund(self):
        # 获取当前时间
        now = datetime.datetime.now()
        # 将时间转换为指定格式
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        yesterday_str = subtract_one_day(now_str,1)
        yesterday_str = subtract_one_day(now_str,2)
        yesterday_str = subtract_one_day(now_str,3)
        yesterday_str = subtract_one_day(now_str,4)
        yesterday_str = subtract_one_day(now_str,5)
        print()



    def analysis_etf(self):
        his_sql = 'select timestamp,symbol,close as close,amount from dev_etf_fund_detail'
        curr_sql = 'select timestamp,symbol,current as close,amount from dev_etf_fund_info'

        # all_data = pd.read_sql(sql=curr_sql, con=sqlExecute.engine)
        # all_data['dif'],all_data['dea'],all_data['MACD'] = talib.MACD(np.array(all_data['close']),fastperiod=12, slowperiod=26, signalperiod=9)
        # print(all_data)


        his_data = pd.read_sql(sql=his_sql, con=sqlExecute.engine)
        curr_data = pd.read_sql(sql=curr_sql, con=sqlExecute.engine)
        all_data = pd.concat([his_data,curr_data],axis=0)
        all_data.drop_duplicates(subset=['timestamp','symbol','close','amount'],keep='first')


        print("开始删除数据.....")
        sql = "truncate table %s ;" % (self.etf_macd_table_name)
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        print("删除数据完成。")

        groups = all_data.groupby('symbol')
        result = pd.DataFrame()
        for name, group in groups:
            group.sort_values(by="timestamp" , inplace=True, ascending=True) 
            print(group)
            # close = group['close'].values
            group['dif'],group['dea'],group['macd'] = talib.MACD(np.array(group['close']),fastperiod=12, slowperiod=26, signalperiod=9)
            
            # # 将MACD值添加到原始DataFrame对象中
            # group['macd'] = macd
            # group['dif'] = signal
            # group['dea'] = hist
            # result = pd.concat([group,result],axis=0)


            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            group['etl_load_time'] = now_str



            group.to_sql("dev_etf_macd_data", sqlExecute.engine, if_exists='append', index=False, chunksize=100)





        
        # all_data['MACD'],all_data['MACDsignal'],all_data['MACDhist'] = talib.MACD(np.array(all_data['close']),fastperiod=12, slowperiod=26, signalperiod=9)



    def run_daily(self):

        df = self.get_etf_code()
        df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
        ts_list = df['timestamp'].drop_duplicates()
        if len(ts_list) >= 2:
            print("Error: 所爬数据出现跨日期异常！")
            print(ts_list)
            exit();

        print("开始删除数据.....")
        sql = "delete from %s where `timestamp` = '%s' " % (self.etf_info_table_name,ts_list[1])
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        print("删除数据完成。")        




    def run_history(self):
        df = self.get_etf_code()
        # print(df.columns)
        df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
        ts_list = df['timestamp'].drop_duplicates()
        if len(ts_list) >= 2:
            print("Error: 所爬数据出现跨日期异常！")
            print(ts_list)
            exit();

        print("开始删除数据.....")
        sql = "delete from %s where `timestamp` = '%s' " % (self.etf_info_table_name,ts_list[1])
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        print("删除数据完成。") 

        df.to_sql(self.etf_info_table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        # df = self.get_etf_detail('SH516510')

        print("开始获取明细数据")
        df = self.read_etf_code()
        print(df)
        etf_codes = df['symbol'].tolist()
        print(etf_codes)
        for etf_code in etf_codes:
            df = self.get_etf_detail(etf_code)
            df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
            df['symbol'] = etf_code
            df.to_sql(self.etf_detail_table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
            print("获取etf：%s" %(etf_code) )
            time.sleep(0.5)







if __name__ == '__main__':
    sc = ScriptETFConfig() # 实例化配置对象
    se = ScriptETF()
    se.set_script_etf_config(sc)
    # df = se.run_history()
    se.analysis_etf()
    # se.get_condition_date('2023-04-01')
    # print(df)
