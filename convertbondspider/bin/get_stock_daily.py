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
    print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))
    sc = ScriptETFConfig() # 实例化配置对象
    se = ScriptETF()
    se.set_script_etf_config(sc)


    se.run_stock_daily()

