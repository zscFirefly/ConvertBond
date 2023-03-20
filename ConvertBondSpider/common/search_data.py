import sys
sys.path.append("..")
import pandas as pd 

from conf.sql_config import *

class SearchData():
    '''sql查询类'''
    def __init__(self,sql):
        self.sql = sql

    def read_data(self):
        data = pd.read_sql(self.sql, sqlExecute.engine)
        return data

    def write_data(self,dataframe,tablename):
        dataframe.to_sql(tablename, sqlExecute.engine,if_exists='append')
        return 0