insert into convert_bond_history
select 
bond_id
,date
,cflg
,ytm_rt
,premium_rt
,convert_value
,price
,volume
,stock_volume
,curr_iss_amt
,amt_change
,turnover_rt
,cnt
,end_dt
,skip_dt
,start_dt
,type
,create_time
,update_time
,null
,null
,null
,null
,null
from tmp_convert_bond_history
where concat(date,bond_id) not in (
	select concat(date,bond_id) from convert_bond_history
)