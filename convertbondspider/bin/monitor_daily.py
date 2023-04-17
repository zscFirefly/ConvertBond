import sys
sys.path.append("..")
import datetime


from core.monitor import *
from common.calender import Calender
from common.search_data import SearchData
from common.wechat import WeChat
from conf.wechat_config import WeChatConfig



def main():
    message = '%s可转债整体数据：\n双低均值：%s\n价格均值：%s\n溢价率均值：%s'
    sql = '''
    select round(avg(price),2) as avg_price
    ,round(avg(premium_rt),2) as avg_premium_rt
    ,round(avg(price+premium_rt),2) as avg_double
    from convert_bond_daily
    where date = CURRENT_DATE
    and price <> 100 and increase_rt <>0
    '''

    sd = SearchData(sql) # 构造sql查询实例
    df = sd.read_data() # 查询数据

    # 构造消息体
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    message = message % (date, df.at[0,'avg_double'], df.at[0,'avg_price'], df.at[0,'avg_premium_rt'])
    
    # 构造飞书配置实例
    fc = FeishuConfig()
    fc.set_user_id('41a6a2ba')
    fc.set_app_id('cli_a3ee5eca19b9900d')
    fc.set_app_secret('sSjQawQabi0sdODSiCxoggeMLhNEWnq7')

    # 构造飞书-监控实例
    fs = FeiShu(fc)
    fs.send_message(message) # 发送消息

    # 构造企业微信配置实例
    wcc = WeChatConfig()
    wcc.set_corpid('wwf61f5f63b0d60a9a')
    wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')

    # 构造企业微信消息推送实例
    wc = WeChat(wcc)
    wc.set_user("ZhengShuoCong") # 设置消息发送人
    wc.set_msgtype("text")
    wc.set_agentid(1000002) # 设置发送应用
    wc.send_message(message) # 设置发送消息




if __name__ == '__main__':
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 判断是否为交易日，如果不为交易日，则不必执行
    ca = Calender(date)
    is_work = ca.get_is_work()
    if is_work == 0:
        print("今日%s，非交易日" % (date))
        exit()

    # 执行代码
    main()
    # app_id = 'cli_a3ee5eca19b9900d'
    # app_secret = 'sSjQawQabi0sdODSiCxoggeMLhNEWnq7'
    # user_id = '41a6a2ba'
    # union_id = 'on_ae6473e89d04c5512829141d428ff083'
    # open_id = 'ou_55a5f41a397faced09f3ed94eace29f5'

