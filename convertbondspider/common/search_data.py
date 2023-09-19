import sys
sys.path.append("..")
import pandas as pd 

from conf.sql_config import *
from sqlalchemy import text

class SearchData():
    '''sql查询类'''
    def __init__(self,sql):
        self.sql = sql

    def read_data(self):
        # data = pd.read_sql(text(self.sql), sqlExecute.engine)
        data = pd.DataFrame(sqlExecute.engine.connect().execute(text(self.sql)))
        return data

    def write_data(self,dataframe,tablename):
        dataframe.to_sql(tablename, sqlExecute.engine,if_exists='append')
        return 0