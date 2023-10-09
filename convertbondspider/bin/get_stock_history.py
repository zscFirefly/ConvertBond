import sys
sys.path.append("..")
import datetime
import pandas as pd 
import time

from conf.sql_config import *
from core.monitor import *
from core.scripy_etf_fund import ScriptETF
from core.script_etf_config import ScriptETFConfig
from core.script_etf_config import * 
from core.read_db_data import * 
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig








if __name__ == '__main__':

    date = datetime.datetime.now().strftime("%Y-%m-%d")


    print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))
    sc = ScriptETFConfig() # 实例化配置对象
    sc.get_xq_a_token()
    se = ScriptETF()
    se.set_script_etf_config(sc)

    rd = readDBData()
    stock_df = rd.get_stock_list()
    for stock in stock_df.to_list():
        print(stock)
        se.run_stock_history(stock)
