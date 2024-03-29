import requests
import json
import pandas as pd
import tushare as ts
import sys
sys.path.append("..")
from conf.sql_config import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from common.calender import Calender




def get_up10per_stock(current_date):
    table_name = 'ods_zt_stock_d'
    #  获取涨停板数据
    url_zt = 'https://push2ex.eastmoney.com/getTopicZTPool?cb=callbackdata9459537&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fbt%3Aasc&date={date}&_=1101682941287'
    url = url_zt.format(date=current_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    response_zt = requests.get(url, headers=headers)
    data_zt = json.loads(response_zt.text[response_zt.text.find("(")+1:response_zt.text.rfind(")")])
    zt_pool = data_zt['data']['pool']
    zt_count = len(zt_pool) #涨停数
    lianban_data = sorted(zt_pool, key=lambda x: -x['lbc'])
    max_lianban = lianban_data[0]['lbc'] if lianban_data else 0 #连板数
    lianban_count = sum(1 for stock in zt_pool if stock['lbc'] >= 2) #最高板

    df = pd.DataFrame(zt_pool)
    df['n_days'] = df['zttj'].apply(lambda x:x['days'])
    df['n_bangs'] = df['zttj'].apply(lambda x:x['ct'])
    df = df.drop('zttj', axis=1)
    df = df.rename(columns={'tshare':'total_market_capital','hs':'change_rate','c':'code','m':'is_first_zt','zdp':'percent','n':'name','lbc':'consist_days','zbc':'zhaban_count','fbt':'first_bang_time','lbt':'last_bang_time','ltsz':'float_market_capital','fund':'bang_amount','hybk':'industry','p':'price'})


    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    df['data_date'] = current_date
    df['create_date'] = date
    df['created_time'] = now_time
    print("开始删除数据.....")
    sql = "delete from %s where `create_date` = '%s' " % (table_name,date)
    with sqlExecute.engine.connect() as connect:
        connect.execute(sql)
    df.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)


def get_down10per_stock(current_date):
    table_name = 'ods_dt_stock_d'
    # 获取跌停板数据
    url_dt = 'https://push2ex.eastmoney.com/getTopicDTPool?cb=callbackdata3558122&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=20&sort=fund%3Aasc&date={date}&_=1701943712045'
    url = url_dt.format(date=current_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    response_dt = requests.get(url, headers=headers)
    data_dt = json.loads(response_dt.text[response_dt.text.find("(")+1:response_dt.text.rfind(")")])
    dt_pool = data_dt['data']['pool']
    df = pd.DataFrame(dt_pool)
    df = df.rename(columns={'fba':'bang_amount','tshare':'total_market_capital','hs':'change_rate','c':'code','m':'is_first_zt','zdp':'percent','n':'name','lbc':'consist_count','zbc':'zhaban_count','fbt':'bang_amount','fbt':'first_bang_time','lbt':'last_bang_time','ltsz':'float_market_capital','fund':'bang_amount','hybk':'industry','p':'price','oc':'open_count','days':'consist_days'})
    # print(df)

    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    df['data_date'] = current_date
    df['create_date'] = date
    df['created_time'] = now_time
    print("开始删除数据.....")
    sql = "delete from %s where `create_date` = '%s' " % (table_name,date)
    with sqlExecute.engine.connect() as connect:
        connect.execute(sql)
    df.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)


def main():
    current_date = datetime.now().strftime('%Y%m%d')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 判断是否为交易日，如果不为交易日，则不必执行
    ca = Calender(date)
    is_work = ca.get_is_work()
    if is_work == 0:
        print("今日%s，非交易日" % (date))
        exit()

    get_up10per_stock(current_date)
    get_down10per_stock(current_date)



    # begin_date = '2023-12-01'
    # end_date = '2023-12-10'
    # # 将字符串转换为datetime对象
    # start_date = datetime.strptime(begin_date, '%Y-%m-%d')
    # end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # # 循环从开始日期到结束日期的每一天
    # current_date = start_date
    # while current_date <= end_date:
    #     # print(current_date.strftime('%Y-%m-%d'))  # 格式化输出日期
    #     ca = Calender(current_date.strftime('%Y-%m-%d'))
    #     is_work = ca.get_is_work()
    #     if is_work == 0:
    #         # print("今日%s，非交易日" % (date))
    #         current_date += timedelta(days=1)  # 每次循环增加一天
    #         continue
    #     else:
    #         print(current_date.strftime('%Y-%m-%d'))

    #         current_date += timedelta(days=1)  # 每次循环增加一天

if __name__ == "__main__":
    main()
