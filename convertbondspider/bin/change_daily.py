import sys
sys.path.append("..")
import pandas as pd 
import requests
import json
import datetime
from datetime import date,timedelta

from common.search_data import SearchData
from common.feishu import FeiShu
from common.wechat import WeChat
from conf.feishu_config import *
from conf.wechat_config import *


class ChangePolicy():

	def __init__(self, date, change_period):
		self.date = date
		self.change_period = change_period

	def caculate(self,top_num):
		daily_sql = '''select  date
			,bond_id
			,bond_nm
			,price
			,premium_rt
			,ytm_rt
			,round(price+premium_rt,2) as double_low
			,year_left
			from convert_bond_daily where date = '%s'
			and year_left >= 1
			and (bond_id <> 100 and increase_rt <> 0)
			and bond_id < 130000
			order by double_low
			limit %s  ''' % (self.date, top_num)
		print(daily_sql)
		sd = SearchData(daily_sql)
		df = sd.read_data()
		return df

	def result_record(self,dataframe,tablename):
		sd = SearchData('')
		sd.write_data(dataframe,tablename)
		return 0


	def if_change(self):
		is_work_sql = '''select is_change from dim_date where day_short_desc = '%s' and is_work = 1 and is_holiday = 0  ''' % (self.date)
		sd = SearchData(is_work_sql)
		print(is_work_sql)

		df = sd.read_data()	

		if len(df) == 0:
			flag = 0
		elif df.at[0,'is_change']%self.change_period == 0:
			flag = 1
		else:
			flag = 0
		return flag





if __name__ == '__main__':

	print("开始执行：%s" % (datetime.datetime.now().strftime('%Y-%m-%d')))

	# 飞书配置
	fc = FeishuConfig()
	fc.set_user_id('41a6a2ba')
	fc.set_app_id('cli_a3ee5eca19b9900d')
	fc.set_app_secret('sSjQawQabi0sdODSiCxoggeMLhNEWnq7')
	fs = FeiShu(fc)

	# 企业微信配置
	wcc = WeChatConfig()
	wcc.set_corpid('wwf61f5f63b0d60a9a')
	wcc.set_corpsecret('YxOnQIESRN_kiKjHjpbAyR1VH__nxqUyBWy-dNfEbj4')
	wc = WeChat(wcc)
	wc.set_user("ZhengShuoCong") # 设置消息发送人
	wc.set_agentid(1000002) # 设置发送应用


	change_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
	# datetime.datetime.now().strftime('%Y-%m-%d') ## 交易日期

	change_period = 30 ## 交易周期

	changepolicy = ChangePolicy(change_date,change_period) # 实例化交易策略。间隔周期
	flag = changepolicy.if_change() # 当日策略
	if flag == 1:
		## 获取策略情况
		df = changepolicy.caculate(20) # 策略数量
		## 记录写入
		changepolicy.result_record(df,'convert_bond_record')
		## 发送飞书
		bond_str = ''
		for i in range(len(df)):
			bond_str = bond_str + str(df.at[i,'bond_id']) + ': ' + str(df.at[i,'bond_nm']) + ' ' + str(df.at[i,'price']) + ', ' + str(df.at[i,'double_low']) + '\n'
		message = '今日需要交易，买入如下：\n%s' % (bond_str)


		fs.send_message(message)
		wc.send_message(message) # 设置发送消息

	else:
		fs.send_message('今日：%s，无需交易。' % ((date.today().strftime("%Y-%m-%d"))))
		wc.send_message('今日：%s，无需交易。' % ((date.today().strftime("%Y-%m-%d"))))
		# df = changepolicy.caculate(20) # 策略数量
		print("End")



