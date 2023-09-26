import sys
sys.path.append("..")
import datetime
import pandas as pd 

from conf.sql_config import *
from core.monitor import *
from core.scripy_etf_fund import ScriptETF
from core.script_etf_config import ScriptETFConfig
from core.script_etf_config import * 
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig







if __name__ == '__main__':

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 判断是否为交易日，如果不为交易日，则不必执行
    ca = Calender(date)
    is_work = ca.get_is_work()
    if is_work == 0:
        print("今日%s，非交易日" % (date))
        exit()

    print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))
    sc = ScriptETFConfig() # 实例化配置对象
    sc.get_xq_a_token()
    se = ScriptETF()
    se.set_script_etf_config(sc)


    se.run_stock_daily()

