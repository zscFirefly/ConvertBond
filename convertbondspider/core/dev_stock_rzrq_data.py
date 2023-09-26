import requests
import requests.utils
from lxml import etree
import pandas as pd
import re
import execjs
import time
import sys
sys.path.append("..")
from conf.sql_config import *


global hexin_v
global headers
 

with open("../conf/token_time.txt",'r') as toke:
	hexin_v = toke.readlines()[0].strip()

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Connection': 'keep-alive',
    'Referer': 'http://data.10jqka.com.cn/market/rzrqgg/code/600975/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'hexin-v': hexin_v,
}
 

def update_time(token_time_text):
	with open("../conf/hexin-v_get.js","r",encoding="utf-8")as f:
	    js = f.read()
	JS = execjs.compile(token_time_text+"\n"+js)    #读取时间拼接进入js代码中
	hexin_v = JS.call("rt.update")
	return hexin_v


def get_data(code,page):
	global hexin_v
	global headers
	# http://data.10jqka.com.cn/market/rzrq/#refCountId=data_55f13c7e_426 网页访问
	url = 'http://data.10jqka.com.cn/ajax/rzrqgg/code/%s/order/desc/page/%s/' % (code,page)
	html = requests.get(url = url,headers=headers, verify=False).text

	## 如果过期，更新hexin_v
	if 'window.location.href' in html:
		url_js = re.compile('<script src="(?P<jsurl>.*?)" type=',re.S)
		url_js_t = "http:"+url_js.search(html).group("jsurl")
		tt = requests.get(url_js_t).text
		token_time_text = tt[:tt.find(";")+1]
		hexin_v = update_time(token_time_text)
		print("hexin_v 过期，更新hexin_v：%s" % (hexin_v))
		with open("../conf/token_time.txt",'w') as toke:
			toke.write(hexin_v)
		time.sleep(0.2)

		headers = {
		    'Accept': 'text/html, */*; q=0.01',
		    'Connection': 'keep-alive',
		    'Referer': 'http://data.10jqka.com.cn/market/rzrqgg/code/600975/',
		    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
		    'hexin-v': hexin_v,
		}
		html = requests.get(url = url,headers=headers, verify=False).text

	return html


def get_total_page(html):
	xpath = '/html/body/div[2]/span/text()'
	element = etree.HTML(html)
	page_total = element.xpath(xpath)
	return page_total[0].split('/')[-1]

# with open('aa.html','w') as f:
# 	f.write(html)

# with open('aa.html','r') as f:
# 	html = f.read()

def wash_data(html):
	element = etree.HTML(html)
	body_xpath = '/html/body/table/tbody/tr[*]'
	data_list = element.xpath(body_xpath)

	finish_df = pd.DataFrame()
	for data in data_list:
		data_details_list = data.xpath('.//td/text()')
		tmp = pd.DataFrame()
		if len(data_details_list) == 11:
			tmp.at[0,'num'] = data_details_list[0]
			tmp.at[0,'date'] = data_details_list[1].strip()
			tmp.at[0,'rz_balance'] = data_details_list[2]
			tmp.at[0,'rz_buy'] = data_details_list[3]
			tmp.at[0,'rz_sales'] = data_details_list[4]
			tmp.at[0,'rz_netbuy'] = data_details_list[5]
			tmp.at[0,'rq_balance'] = data_details_list[6]
			tmp.at[0,'rq_buy'] = data_details_list[7]
			tmp.at[0,'rq_sales'] = data_details_list[8]
			tmp.at[0,'rq_netbuy'] = data_details_list[9]
			tmp.at[0,'rzrq_balance'] = data_details_list[10]
			finish_df = pd.concat([finish_df,tmp],axis=0)

		else:
			print("数据异常")
	return finish_df


def read_dz_data():
    sql = '''select code from stock_dwd_dz_data where code > '600756' group by code '''
    code_list = pd.read_sql(sql,sqlExecute.engine)
    return code_list['code']


def run_single_code(code):
	# code = '600975'
	page = 1
	# 先爬第一页
	html = get_data(code,page)
	total_df = wash_data(html)
	total_page = get_total_page(html)


	for i in range(2,int(total_page)+1):
		print("get page %s" % (i))
		html = get_data(code,i)
		df = wash_data(html)
		total_df = pd.concat([total_df,df],axis=0)
		time.sleep(0.1)

	table_name = 'stock_ods_rzrq_data'
	total_df['code'] = code
	total_df.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)



def main():
	code_list = read_dz_data()
	for code in code_list:
		print("get code: %s" % (code))
		try:
			run_single_code(code)
		except Exception as e:
			print("code:%s 非融资融券标的" % (code))
		

if __name__ == '__main__':
	main()

