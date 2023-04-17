import sys
sys.path.append("..")
import datetime


from core.monitor import *
from core.scripy_etf_fund import ScriptETF
from core.script_etf_config import ScriptETFConfig
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig



if __name__ == '__main__':
    print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))
    sc = ScriptETFConfig() # 实例化配置对象
    se = ScriptETF()
    se.set_script_etf_config(sc)
    se.run_daily()

    wcc = WeChatConfig()
    wcc.set_corpid('wwf61f5f63b0d60a9a')
    wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')
    wc = WeChat(wcc)
    wc.set_user("ZhengShuoCong")
    wc.set_msgtype("text")
    wc.set_agentid(1000002)
    wc.send_message("今日ETF爬虫完成")

