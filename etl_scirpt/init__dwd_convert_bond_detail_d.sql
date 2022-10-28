use convert_bond;
truncate table convert_bond.dwd_convert_bond_detail_d;
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
union all 
select 
a.bond_id
, a.date
, b.bond_nm
, a.price
, a.premium_rt
, case when a.ytm_rt = '-' then null else a.ytm_rt end as ytm_rt
, a.curr_iss_amt
, a.volume
, case when a.turnover_rt = '-' then null else a.turnover_rt end as turnover_rt
, a.convert_value
, now() etl_load_time
from convert_bond.convert_bond_history a 
left join convert_bond.convert_bond_info b on a.bond_id = b.bond_id 
;
