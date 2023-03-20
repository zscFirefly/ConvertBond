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



;

INSERT into convert_bond_loopback
select 
bond_id
,date
,price
,premium_rt
,ytm_rt
,sort_result
,now()
,now()
from (
	select 
	bond_id
	,date
	,price
	,premium_rt
	,ytm_rt
	,case when @dept_no_t != x.bond_id then @row_num_t := 1
	else @row_num_t := @row_num_t + 1 end as sort_result
	, @dept_no_t := x.bond_id as dept_no
	from convert_bond_history x,
		(select @dept_no_t := '') as t1,
		(select @row_num_t := 0) as t2
	order by bond_id,date desc 
)a 





