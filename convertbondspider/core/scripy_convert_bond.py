import sys
sys.path.append("..")
import requests
import pandas as pd
import datetime
import time

from conf.sql_config import *
from core.script_config import * 


class ScriptBase():
    '''爬虫基础类'''
    def __init__(self):
        self.script_config = None

    def set_script_config(self,script_config):
        self.script_config = script_config


    def util_to_df(self,debt_json):
        ## 将获取下来的数据由json转化为dataframe
        finish_data = pd.DataFrame()
        # print(debt_json)
        for debt in debt_json:
            # print(debt)
            tmp_data = pd.DataFrame(debt,index=[0]) # 爬code的时候，记得修改
            # tmp_data = pd.DataFrame(debt['cell'],index=[0])
            finish_data = finish_data.append(tmp_data,ignore_index=True)
        return finish_data

    def util_to_df_fordetail(self,debt_json):
        ## 将获取下来的数据由json转化为dataframe
        finish_data = pd.DataFrame()
        for debt in debt_json:
            tmp_data = pd.DataFrame(debt['cell'],index=[0])
            finish_data = finish_data.append(tmp_data,ignore_index=True)
        return finish_data        


    def if_data(self,ori_data):
        debt_json = ori_data['rows']
        if len(debt_json) == 0:
            return False
        else:
            return True

    def get_convert_code(self,dtype):
        '''
        爬取可转债主页信息
        online：cb_list、outline：delisted
        '''
        # dept_type = {'online':'list_new','outline':'delisted'}
        dept_type = {'online':'list','outline':'delisted'}
        url = 'https://www.jisilu.cn/webapi/cb/%s/' % (dept_type[dtype])
        print(self.script_config.get_headers())
        response = requests.post(url=url, headers=self.script_config.get_headers(), cookies=self.script_config.get_cookies())
        debt_json = response.json()['data']
        df = self.util_to_df(debt_json)
        return df



    def get_all_convert_code(self):
        '''获取所有可转债代码并保存'''
        pass


class ConvertBondDaily(ScriptBase):
    '''每日数据获取类'''
    def daily(self):
        finish_data = self.get_convert_code('online')
        print(finish_data)
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        finish_data['date'] = date
        # finish_data.to_csv("debt_code"+now_time+".csv",index=False)
        print("开始删除数据.....")
        sql = "delete from convert_bond_daily where `date` = '%s' " % (date)
        with sqlExecute.engine.connect() as connect:
            connect.execute(sql)
        # sqlExecute.executeSQL(sql)

        print("删除数据成功.")
        print("开始写入数据.....")
        finish_data.to_sql('convert_bond_daily', sqlExecute.engine, if_exists='append', index=False, chunksize=100)
        print("写入数据成功")


    def run(self):
        self.daily()

        

class ConvertBondHistory(ScriptBase):
    '''爬历史数据类'''

    def get_all_convert_code(self):
        '''重写获取可转债代码方法，'''
        finish_data = pd.DataFrame()
        online = self.get_convert_code('online')
        outline = self.get_convert_code('outline')
        finish_data = finish_data.append(online,ignore_index=True)
        finish_data = finish_data.append(outline,ignore_index=True)
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # finish_data[['bond_id','bond_nm']].to_csv("debt_code.csv",index=False)
        finish_data[['bond_id','bond_nm']].to_sql('tmp_convert_bond_info_0320', sqlExecute.engine, if_exists='append', index=False, chunksize=100)


    def read_debt_code(self):
        # data = pd.read_csv('debt_code.csv')
        data = pd.read_sql(sql='select bond_id,bond_nm from tmp_convert_bond_info_0320', con=sqlExecute.engine)
        return data

    def get_convert_detail(self,id):
        # 爬明细数据
        url = 'https://www.jisilu.cn/data/cbnew/detail_hist/%s?___jsl=LST___t=1659969040759' % (id)
        response = requests.post(url=url, headers=self.script_config.get_headers(), cookies=self.script_config.get_cookies(),data=self.script_config.get_data())
        return response.json()

    def standard_data(self,data):
        '''标准化数据'''
        debt_json = data['rows']
        df = self.util_to_df_fordetail(debt_json)

        # 'bond_id':id
        # 'last_chg_dt'：日期
        # 'ytm_rt'：到期税前收益率
        # 'premium_rt'：转股溢价率
        # 'convert_value'：转股价值
        # 'price'：收盘价
        # 'volume'：成交额
        # 'stock_volume'：xxx
        # 'curr_iss_amt'：剩余规模
        # 'amt_change'：
        # 'turnover_rt'：换手率
        # print(finish_data)
        rename_dict = {
            'last_chg_dt':'date', 
            '_cnt':'cnt', 
            '_start_dt':'start_dt', 
            '_end_dt':'end_dt', 
            '_skip_dt': 'skip_dt', 
            '_type': 'type', 
            }
        df.rename(columns=rename_dict, inplace = True)
        df['ytm_rt'] = df['ytm_rt'].apply(lambda x:x.split('%')[0])
        df['premium_rt'] = df['premium_rt'].apply(lambda x:x.split('%')[0])


        return df[['bond_id','date','ytm_rt','premium_rt','price','convert_value','turnover_rt','volume','stock_volume','curr_iss_amt','amt_change','cnt','end_dt','start_dt','skip_dt','type','cflg']]



    def init(self):
        table_name = 'tmp_convert_bond_history_0320'
        # now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # FILE_NAME = "debt_detail"+now_time+".csv" # 文件名称
        # sql = 'truncate table %s;' % (table_name)
        # with sqlExecute.engine.connect() as connect:
        #     connect.execute(sql)

        all_data = pd.DataFrame()
        self.get_all_convert_code() # 爬可转债代码，存到csv。
        debt_code = self.read_debt_code() # 读取已存csv的code数据
        for num in range(len(debt_code)):# 
            print("爬取第%s个转债" % (num))
            bond_id = debt_code.at[num,'bond_id']
            ori_data = self.get_convert_detail(bond_id) # 获取可转债数据明细
            time.sleep(0.5)
            if self.if_data(ori_data): # 检查json数据是否合法
                data = self.standard_data(ori_data) # 标准化数据
                data.to_sql(table_name, sqlExecute.engine, if_exists='append', index=False, chunksize=100)
                # all_data = all_data.append(data,ignore_index=True)
                # all_data.to_csv(FILE_NAME,index=False)
            else:
                print("Not data:", bond_id)

    def run(self):
        self.init()
        # self.read_debt_code()


if __name__ == '__main__':
#     cb = ConvertBondDaily()
#     cb.run()
    sc = ScriptConfig()
    cb = ConvertBondHistory()
    cb.set_script_config(sc)
    cb.run()
