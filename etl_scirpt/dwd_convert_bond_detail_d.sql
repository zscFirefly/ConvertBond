use convert_bond;
delete from dwd_convert_bond_detail_d where date = CURRENT_DATE;
insert into dwd_convert_bond_detail_d
select 
bond_id
, date
, bond_nm
, price
, premium_rt
, ytm_rt
, curr_iss_amt
, volume
, turnover_rt
, convert_value
, now() etl_load_time
from convert_bond_daily
where date = CURRENT_DATE
;