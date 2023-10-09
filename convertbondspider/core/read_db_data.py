import sys
sys.path.append("..")
import datetime
import pandas as pd 

from conf.sql_config import *



class readDBData():
	def __init__(self):
		pass 

	def get_stock_list(self):
		sql = '''  select symbol from stock_ods_stock_date group by symbol  '''
		data = pd.read_sql(sql=sql, con=sqlExecute.engine)
		return data['symbol']




if __name__ == '__main__':
	rd = readDBData()
	stock_df = rd.get_stock_list()
	for stock in stock_df.to_list():
		print(stock)

