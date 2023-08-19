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


def get_quote_data():
    sql = '''
    select distinct concat('SH',code) as code from sh_convertbond_publish_info
    union all
    select distinct concat('SZ',secCode) as code from convertbond_publish_info cpi
    '''
    code_list = pd.read_sql(sql,sqlExecute.engine)
    return code_list['code']




if __name__ == '__main__':
    print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))
    sc = ScriptETFConfig() # 实例化配置对象
    se = ScriptETF()
    se.set_script_etf_config(sc)

    tablename = 'convertbond_publish_quote_data'

    code_list = get_quote_data()
    print(code_list)

    for code in code_list:
        print("get code " + str(code))
        df = se.get_etf_detail(code)
        df['code'] = code
        df.to_sql(tablename, sqlExecute.engine, if_exists='append', index=False, chunksize=100)

