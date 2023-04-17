import sys
sys.path.append("..")
import pandas as pd 

from common.search_data import SearchData

class Calender():

	def __init__(self,date):
		self.date = date

	def get_is_work(self):
		is_work_sql = '''select is_work from dim_date where day_short_desc = '%s' ''' % (self.date)
		sd = SearchData(is_work_sql)
		df = sd.read_data()
		return df.at[0,'is_work']

	def get_last_work_day(self):
		## 先判断是否为工作日。如果是工作日，直接取上一个交易日，如果非工作日，取当前结果的第一个工作日。
		is_work = self.get_is_work()
		if is_work == 1:
			last_work_sql = '''select day_short_desc as last_work_date from dim_date where day_short_desc <= '%s' and is_work = 1 order by day_short_desc desc limit 1,1''' % (self.date)
			sd = SearchData(last_work_sql)
			df = sd.read_data()
			return df.at[0,'last_work_date']
		else:
			last_work_sql = '''select day_short_desc as last_work_date from dim_date where day_short_desc <= '%s' and is_work = 1 order by day_short_desc desc limit 0,1''' % (self.date)
			sd = SearchData(last_work_sql)
			df = sd.read_data()
			return df.at[0,'last_work_date']




if __name__ == '__main__':
	ca = Calender('2022-11-05')
	is_work = ca.get_is_work()
	last_work_date = ca.get_last_work_day()
	print(last_work_date)


