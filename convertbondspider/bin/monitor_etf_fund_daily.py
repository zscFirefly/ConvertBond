import sys
sys.path.append("..")
import datetime


from core.monitor import *
from core.analy_etf_fund import AnalyETF
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig




if __name__ == '__main__':
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    # 判断是否为交易日，如果不为交易日，则不必执行
    ca = Calender(date_str)
    is_work = ca.get_is_work()
    if is_work == 0:
        print("今日%s，非交易日" % (date))
        exit()
    else:
        last_work_date = ca.get_last_work_day()

    an = AnalyETF()
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


