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
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig


class AnalyETF():
    def __init__(self):
        self.script_etf_config = None
        self.etf_info_table_name = 'dev_etf_fund_info'
        self.etf_detail_table_name = 'dev_etf_fund_detail'
        self.etf_macd_table_name = 'dev_etf_macd_data'

    def set_script_etf_config(self,script_etf_config):
        self.script_etf_config = script_etf_config


    def get_condition_data(self,date):
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
        and e < 0
        and amount > 100000000
        and close < 10
        '''.format(date_df.at[0,'timestamp'],date_df.at[1,'timestamp'],date_df.at[2,'timestamp'],date_df.at[3,'timestamp'],date_df.at[4,'timestamp'],date_df.at[5,'timestamp'],date_df.at[6,'timestamp'],table_name = self.etf_macd_table_name)
        df = pd.read_sql(sql=sql, con=sqlExecute.engine)
        return df


    def analysis_etf(self):

        his_sql = 'select timestamp,symbol,close as close,amount from dev_etf_fund_detail order by timestamp'
        curr_sql = 'select timestamp,symbol,current as close,amount from dev_etf_fund_info'

        # his_sql = 'select timestamp,symbol,close as close,amount,macd as macd_org,dea as dea_org,dif as dif_org from dev_etf_fund_detail  where symbol = "SH515220" order by timestamp'
        # all_data = pd.read_sql(sql=his_sql, con=sqlExecute.engine)
        # all_data['dif'],all_data['dea'],all_data['MACD'] = talib.MACD(np.array(all_data['close']),fastperiod=12, slowperiod=26, signalperiod=9)
        # all_data['MACD'] = all_data['MACD'] * 2
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
            group['macd'] = group['macd'] * 2
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            group['etl_load_time'] = now_str

            group.to_sql(self.etf_macd_table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        print("analysis_etf done!!")



    def get_message(self,df):
        if len(df) == 0:
            msg = '''今日ETF无明显机会。'''
        else:
            msg = '''今日ETF潜在机会:\n'''
            data = ''''''
            for i in range(len(df)):
                data = data + '' + df.at[i,'symbol'] + ' ' + str(round(df.at[i,'f'],3)) + ' ' + str(round(df.at[i,'g'],3)) + ' ' + str(round(df.at[i,'close'],1)) + ' ' + str(round(df.at[i,'amount']/100000000,1)) + '\n'
            msg = msg + data
        return msg    
 

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
    an = AnalyETF()
    # an.analysis_etf()
    # df = se.run_history()
    # se.analysis_etf()

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    ca = Calender(now_str)
    is_work = ca.get_is_work()
    if is_work != 1:
        print("非交易日")
    else:
        last_work_date = ca.get_last_work_day()

    df = an.get_condition_data(last_work_date)
    msg = an.get_message(df)
    print(msg)

    wcc = WeChatConfig()
    wcc.set_corpid('wwf61f5f63b0d60a9a')
    wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')
    wc = WeChat(wcc)
    wc.set_user("ZhengShuoCong")
    wc.set_msgtype("text")
    wc.set_agentid(1000002)
    wc.send_message(msg)


