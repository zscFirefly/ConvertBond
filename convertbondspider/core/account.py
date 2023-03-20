import sys
sys.path.append("..")
import pandas as pd 
import datetime 
from common.search_data import SearchData
from common.calender import Calender

class Account():
    """docstring for Account"""
    def __init__(self, account):
        self.account = account
        self.hold_bond = None
        self.balance = account
        self.begin_date = None # 开始回测时间
        self.hold_time = 30 # 倒计时  
        self.hold_num = None # 持有数量
        self.hold_value = 0

    def set_begin_date(self,begin_date):
        self.begin_date = begin_date

    def set_hold_time(self,hold_time):
        self.hold_time = hold_time

    def set_hold_num(self,hold_num):
        self.hold_num = hold_num


    def change(self, date):
        ''' when hold_time is 0, to be change '''
        # 买入债券
        # print("change ways")
        # print("账户金额：" + str(self.account))
        # print("账户余额：" + str(self.balance))
        # print("卖前持仓金额：" + str(self.hold_value))
        # print("卖前持仓：")
        # print(self.hold_bond)

        self.balance = self.hold_value + self.balance # 先计算账户
        ## rn 表示强赎前第n天。
        sql = '''select bond_id,price from (select bond_id,price from convert_bond.convert_bond_loopback where date = '%s' and rn > 40 order by 0.8*premium_rt+1.2*price+1.0*ytm_rt limit 20) a where a.price < 130''' % (date)
        # print(sql)
        sd = SearchData(sql)
        self.hold_bond = sd.read_data()
        self.hold_bond['hold'] = 0


        # print(self.hold_bond,self.balance)
        sign = 0
        # 循环买入，直到账户没钱。
        while sign == 0:
            for idx in range(len(self.hold_bond)):
                if self.balance > float(self.hold_bond.at[idx,'price'])*10: # 如果够买，则买入
                    self.balance = self.balance - float(self.hold_bond.at[idx,'price'])*10
                    self.hold_bond.at[idx,'hold'] += 10
                else:
                    sign = 1

        print("买后持仓：")
        print(self.hold_bond)


    def caculate(self, date):
        '''计算市值'''
        param = ','.join(self.hold_bond['bond_id'].astype(str).tolist())
        sql = '''select bond_id,price from convert_bond_loopback where date = '%s' and bond_id in (%s) and bond_name not in ('紫银转债','光大转债','苏银转债','齐鲁转债','苏农转债','苏行转债','杭银转债','成银转债','青农转债')  ''' % (date, param)

        sd = SearchData(sql)
        res = sd.read_data()
        # print(self.balance)


        # 如果大于130，则卖出。
        tmp = pd.merge(self.hold_bond,res,how='left',on='bond_id')
        tmp = tmp[['bond_id','hold','price_y','price_x']]
        tmp.fillna(method='backfill',axis=1) 
        tmp['value'] = tmp['hold'].astype(float) * tmp['price_y'].astype(float)

        for i in range(len(tmp)):
            if float(tmp.at[i,'price_y']) >= 130 and int(tmp.at[i,'hold']) > 0:
                self.balance += tmp.at[i,'value']
                self.hold_bond.at[i,'hold'] = 0
                tmp.at[i,'value'] = 0

        ## 卖掉后，要去掉tmp的值
        
        self.hold_value = tmp['value'].astype(float).sum()
        self.account = self.hold_value + self.balance
        print(str(date) + ": " + str(self.hold_value) + "\t" + str(self.balance) + "\t" + str(self.account))







    def action(self,begin_date,end_date):
        '''回测行为'''
        begin_date=datetime.datetime.strptime(begin_date,'%Y-%m-%d')
        end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
        this_date = begin_date

        flag = self.hold_time
        sign = 0
        hold_date = 0 # 当前持有日期


        # 日期范围内循环
        while this_date < end_date:
            this_date_str = datetime.datetime.strftime(this_date,'%Y-%m-%d')
            ca = Calender(this_date_str)
            is_work = ca.get_is_work()
            ## 如果非交易日，下一天。
            if is_work == 0:
                print("今日%s，非交易日" % (this_date_str))
                this_date = this_date+datetime.timedelta(days=1)
                continue


            # 交易日，当前持有第几天，是否要触发换票
            if sign == 0: # 第一次买入
                self.change(this_date_str) 
                sign += 1
            hold_date += 1
            if hold_date == self.hold_time:
                print("今日%s,交易" % (this_date_str))
                self.change(this_date_str)
                self.caculate(this_date_str)
                hold_date = 0
            else :
                print("今日%s,持仓第%s天" % (this_date_str,hold_date))
                self.caculate(this_date_str)


            this_date = this_date+datetime.timedelta(days=1)






        # print(next_date)
        # ca = Calender(date)
        # is_work = ca.get_is_work()
        # if is_work == 0:
        #     print("今日%s，非交易日" % (date))
        #     exit()
        # 







def main():
    acc = Account(100000.00)
    acc.action('2021-01-10','2022-09-01')


if __name__ == '__main__':
    main()