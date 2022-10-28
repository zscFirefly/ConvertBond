use convert_bond;
delete from convert_bond.dwd_convert_bond_detail_d where date = CURRENT_DATE;
insert into convert_bond.dwd_convert_bond_detail_d
select 
bond_id
, date
, bond_nm
, price
, premium_rt
, case when ytm_rt = '-' then null else ytm_rt end as ytm_rt
, curr_iss_amt
, volume
, case when turnover_rt = '-' then null else turnover_rt end as turnover_rt
, convert_value
, now() etl_load_time
from convert_bond.convert_bond_daily
where date = CURRENT_DATE
;