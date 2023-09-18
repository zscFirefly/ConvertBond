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
# import talib
import numpy as np
pd.set_option('expand_frame_repr', False)

from conf.sql_config import *
from core.script_etf_config import * 
from core.script_etf_config import ScriptETFConfig
from core.user_login import *
from common.calender import Calender
from datetime import datetime, timedelta
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig


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

    def util_quote_to_df(self,debt_json):
        ## 将获取下来的数据由json转化为dataframe
        finish_data = pd.DataFrame()
        # print(debt_json)
        for debt in debt_json:
            # debt['etf_types'] = str(debt['etf_types'])
            finish_data = pd.concat([finish_data,pd.DataFrame(debt,index=[1])],axis=0)

        return finish_data


    def change_timestamp2date(self,ts_ms):
        '''将时间戳转化为日期'''
        ts_sec = ts_ms / 1000  # 转换为秒
        utc_datetime = datetime.utcfromtimestamp(ts_sec)  # 转换为UTC时间
        local_datetime = utc_datetime + timedelta(hours=8)  # 转换为当地时间（北京时间）
        date_str = local_datetime.strftime('%Y-%m-%d')  # 转换为%Y-%m-%d格式的字符串
        return date_str

    def get_etf_code(self):
        '''获取所有etf列表信息'''
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

    def get_quote_code(self):
        '''获取当日股票列表信息'''

        ## 正序获取（因为最多只能5000条，超过5000条就报错）
        url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'
        params = (
            ('page', '1'), # page页数
            ('size', '5000'), #size 每页长度，设置5000则可以一口气爬下所有
            ('order', 'asc'),
            ('order_by', 'percent'),
            ('type', 'sh_sz'),
            # ('_', '1591462668100'),
            # ('market', 'CN'),
            # ('orderby', 'percent'),

        )

        response = requests.get(url = url,params=params,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        quote_list = response.json()['data']['list']
        df_asc = self.util_quote_to_df(quote_list)
        print(df_asc)
        print("正序完成....")

        ## 倒序获取
        params = (
            ('page', '1'), # page页数
            ('size', '5000'), #size 每页长度，设置5000则可以一口气爬下所有
            ('order', 'desc'),
            ('order_by', 'percent'),
            ('type', 'sh_sz'),

        )
        response = requests.get(url = url,params=params,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        quote_list = response.json()['data']['list']
        df_desc = self.util_quote_to_df(quote_list)
        print(df_desc)
        print("倒序完成....")


        df = pd.DataFrame()
        df= pd.concat([df_asc,df_desc],axis=0)

        df.drop_duplicates(subset=['symbol'],keep='first',inplace=True)
        print("去重完成....")
        print(df.columns)

        return df[['symbol', 'net_profit_cagr', 'north_net_inflow', 'ps', 'type','percent', 'has_follow', 'tick_size', 'pb_ttm', 'float_shares','current', 'amplitude', 'pcf', 'current_year_percent','float_market_capital', 'north_net_inflow_time', 'market_capital','dividend_yield', 'lot_size', 'roe_ttm', 'total_percent', 'percent5m','income_cagr', 'amount', 'chg', 'issue_date_ts', 'eps','main_net_inflows', 'volume', 'volume_ratio', 'pb', 'followers','turnover_rate', 'mapping_quote_current', 'first_percent', 'name','pe_ttm', 'dual_counter_mapping_symbol', 'total_shares','limitup_days']]



    def get_quote_info(self,code):
        '''获取所有股票基本信息'''
        url = 'https://stock.xueqiu.com/v5/stock/quote.json'
        params = {
            'symbol': code,
            'extend': 'detail',
        }

        response = requests.get(url = url,params=params,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        # print(response.json())
        quote_info = response.json()['data']['quote']
        # print(quote_info)
        df = pd.DataFrame(quote_info,index=[0])
        return df[['current_ext','symbol','volume_ext','high52w','delayed','type','tick_size','float_shares','limit_down','no_profit','high','float_market_capital','timestamp_ext','lot_size','lock_set','weighted_voting_rights','chg','eps','last_close','profit_four','volume','volume_ratio','profit_forecast','turnover_rate','low52w','name','exchange','pe_forecast','total_shares','status','code','goodwill_in_net_assets','avg_price','percent','weighted_voting_rights_desc','amplitude','current','current_year_percent','issue_date','sub_type','low','is_registration_desc','no_profit_desc','market_capital','dividend','dividend_yield','currency','navps','profit','timestamp','pe_lyr','amount','pledge_ratio','traded_amount_ext','is_registration','pb','limit_up','pe_ttm','time','open']]


    def get_etf_detail(self,code):
        '''获取所有etf的k线图数据'''
        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?"
        data = {
            'symbol': code, 
            'begin': str(int(time.time() * 1000)), 
            'period': 'day', 
            'type': 'before', 
            'count': '-1000', 
            'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance,macd'
        } 

        response = requests.get(url = url,params=data,cookies=self.script_etf_config.get_cookies(),headers=self.script_etf_config.get_headers())
        print(response.json())
        res_column = response.json()['data']['column']
        res_items = response.json()['data']['item']
        json_list = []
        df = pd.DataFrame()
        for item in res_items:
            zipped= dict(zip(res_column,item))
            df = pd.concat([df,pd.DataFrame(zipped,index=[1])],axis=0)
        return df


    def read_etf_code(self,date):
        '''爬取历史明细数据时，读取etf列表'''
        # today = '2023-04-14'
        sql = '''select symbol from dev_etf_fund_info  where timestamp = '%s' ;''' % (today)
        print(sql)
        data = pd.read_sql(sql=sql, con=sqlExecute.engine)
        return data



    def run_stock_daily(self):
        df = self.get_quote_code()
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%s")
        df['timestamp'] = timestamp
        df['date'] = date

        tablename = 'stock_ods_stock_date'
        print("开始删除%s的数据....."%(date))
        sql = "delete from %s where `date` = '%s' " % (tablename,date)
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        df.to_sql(tablename, sqlExecute.engine, if_exists='append', index=False, chunksize=100)

        wash_df = df[['symbol','type','name','percent','current','amount','market_capital','float_market_capital','turnover_rate','chg','volume_ratio','total_shares','date']]
        tablename = 'stock_dwd_stock_date'
        print("开始删除%s的数据....."%(date))
        sql = "delete from %s where `date` = '%s' " % (tablename,date)
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        wash_df.to_sql(tablename, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        print("数据存储完成")



    def run_daily(self):

        df = self.get_etf_code()
        df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
        ts_list = df['timestamp'].drop_duplicates()
        if len(ts_list) >= 2:
            print("Error: 所爬数据出现跨日期异常！")
            print(ts_list)
            exit();


        print("开始删除%s的数据....."%(ts_list[1]))
        sql = "delete from %s where `timestamp` = '%s' " % (self.etf_info_table_name,ts_list[1])
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        print("删除数据完成。")
        print(df)
        df.to_sql(self.etf_info_table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        print("存储数据完成")





    def run_history(self):
        df = self.get_etf_code()
        # print(df.columns)
        df['timestamp'] = df['timestamp'].apply(self.change_timestamp2date)
        ts_list = df['timestamp'].drop_duplicates()
        if len(ts_list) >= 2:
            print("Error: 所爬数据出现跨日期异常！")
            print(ts_list)
            exit();

        print("开始删除%s的数据....."%(ts_list[1]))
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

    def get_message(self,df):
        msg = '''今日ETF潜在机会:\n'''
        data = ''''''
        for i in range(len(df)):
            data = data + '' + df.at[i,'symbol'] + ' ' + str(round(df.at[i,'f'],3)) + ' ' + str(round(df.at[i,'g'],3)) + ' ' + str(round(df.at[i,'close'],1)) + ' ' + str(round(df.at[i,'amount']/100000000,1)) + '\n'

        return msg + data            
 

    def main(self):
        # message = r'''hello world\n <a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>'''
        message = "ssd"
        # message = '''aaa'''
        wcc = WeChatConfig()
        wcc.set_corpid('wwf61f5f63b0d60a9a')
        wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')

        # 构造企业微信消息推送实例
        wc = WeChat(wcc)
        wc.set_user("ZhengShuoCong") # 设置消息发送人
        wc.set_agentid(1000002) # 设置发送应用
        wc.send_message(message) # 设置发送消息





if __name__ == '__main__':
    sc = ScriptETFConfig() # 实例化配置对象
    se = ScriptETF()
    se.set_script_etf_config(sc)
    # se.run_daily()

    se.run_stock_daily()
    # print(df)



    # se.analysis_etf()
    # df = se.get_condition_data('2023-04-01')

    # msg = se.get_message(df)
    # wcc = WeChatConfig()
    # wcc.set_corpid('wwf61f5f63b0d60a9a')
    # wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')
    # wc = WeChat(wcc)
    # wc.set_user("ZhengShuoCong")
    # wc.set_msgtype("text")
    # wc.set_agentid(1000002)
    # wc.send_message(msg)


