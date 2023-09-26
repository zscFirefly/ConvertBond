import requests
import re
import json
import pandas as pd 
import time
import sys 

sys.path.append("..")
from conf.sql_config import *


def get_data(page,size):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    data = {
        'callback':'jQuery1123019058759780733836_1695370375552',
        'sortColumns':'ISSUE_DATE',
        'sortTypes':'-1',
        'pageSize':size,
        'pageNumber':page,
        'reportName':'RPT_SEO_DETAIL',
        'columns':'ALL',

    }

    ## 实际网址：https://data.eastmoney.com/other/dxzf.html
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    response = requests.post(url = url, headers=headers,data=data)

    return response.text+'smart_flag'



def wash_data(jquery):

    json_str = re.findall(r'jQuery1123019058759780733836_1695370375552\((.*?)\);smart_flag',jquery,re.S)[0]

    data_json = json.loads(json_str)

    data_list = data_json['result']['data']

    finish_df = pd.DataFrame()
    for data in data_list:
        finish_df = pd.concat([pd.DataFrame(data,index=[0]),finish_df],axis=0)

    # print(finish_df)

    return finish_df


def main():

    finish_data = pd.DataFrame()
    size = 50
    total_size = 111 # 手动设定总页数

    for page in range(1,total_size+1):
        print('get page %s' % (page))
        jquery = get_data(page,size)
        tmp = wash_data(jquery)
        finish_data = pd.concat([finish_data,tmp],axis=0)
        time.sleep(0.5)
    
    table_name = 'stock_ods_dz_data'

    finish_data.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)



if __name__ == '__main__':
    main()

