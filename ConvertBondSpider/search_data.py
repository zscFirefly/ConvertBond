import pandas as pd 
from sql_config import *

class SearchData():
    '''sql查询类'''
    def __init__(self,sql):
        self.sql = sql

    def read_data(self):
        data = pd.read_sql(self.sql, sqlExecute.engine)
        return data