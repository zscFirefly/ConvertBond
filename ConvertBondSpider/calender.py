import pandas as pd 
from search_data import SearchData

class Calender():

	def __init__(self,date):
		self.date = date

	def get_is_work(self):
		is_work_sql = '''select is_work from dim_date where day_short_desc = '%s' ''' % (self.date)
		sd = SearchData(is_work_sql)
		df = sd.read_data()
		return df.at[0,'is_work']



if __name__ == '__main__':
	ca = Calender('2022-11-05')
	is_work = ca.get_is_work()
	print(is_work)


