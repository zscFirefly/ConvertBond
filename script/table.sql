create table convert_bond_daily (
`date` date comment '快照日期',
bond_id int(8) comment '转债代码',
bond_nm varchar(30) comment '',
bond_py varchar(30) comment '',
price varchar(30) comment '',
increase_rt varchar(30) comment '',
stock_id varchar(30) comment '',
stock_nm varchar(30) comment '',
stock_py varchar(30) comment '',
sprice varchar(30) comment '',
sincrease_rt varchar(30) comment '',
pb varchar(30) comment '',
convert_price varchar(30) comment '',
convert_value varchar(30) comment '',
convert_dt varchar(30) comment '',
premium_rt varchar(30) comment '',
dblow varchar(30) comment '',
sw_cd varchar(30) comment '',
market_cd varchar(30) comment '',
btype varchar(30) comment '',
list_dt varchar(30) comment '',
qflag2 varchar(30) comment '',
owned varchar(30) comment '',
hold varchar(30) comment '',
bond_value varchar(30) comment '',
rating_cd varchar(30) comment '',
option_value varchar(30) comment '',
put_convert_price varchar(30) comment '',
force_redeem_price varchar(30) comment '',
convert_amt_ratio varchar(30) comment '',
fund_rt varchar(30) comment '',
short_maturity_dt varchar(30) comment '',
year_left varchar(30) comment '',
curr_iss_amt varchar(30) comment '',
volume varchar(300) comment '',
svolume varchar(300) comment '',
turnover_rt varchar(300) comment '',
ytm_rt varchar(300) comment '',
put_ytm_rt varchar(300) comment '',
noted varchar(300) comment '',
bond_nm_tip varchar(300) comment '',
redeem_icon varchar(300) comment '',
last_time varchar(300) comment '',
qstatus varchar(300) comment '',
margin_flg varchar(300) comment '',
sqflag varchar(300) comment '',
pb_flag varchar(300) comment '',
adj_cnt varchar(300) comment '',
adj_scnt varchar(300) comment '',
convert_price_valid varchar(300) comment '',
convert_price_tips varchar(300) comment '',
convert_cd_tip varchar(300) comment '',
ref_yield_info varchar(300) comment '',
adjusted varchar(300) comment '',
orig_iss_amt varchar(300) comment '',
price_tips varchar(300) comment '',
redeem_dt varchar(300) comment '',
real_force_redeem_price varchar(300) comment '',
option_tip varchar(300) comment '',
notes varchar(300) comment '',
create_time timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
update_time timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次修改时间'
) ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债每日数据表'



;

create table convert_bond_info (
	bond_id int(30) comment 'id',
	bond_nm varchar(30) comment '可转债名称',
	create_time timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
	update_time timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次修改时间'
) ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债id名称表'
;


create table convert_bond_history (
	bond_id int(30) comment 'id',
	`date` varchar(30) comment '日期', 
	cflg varchar(30) comment 'cflg',
	ytm_rt varchar(30) comment '到期税前收益率',
	premium_rt varchar(30) comment '转股溢价率',
	convert_value varchar(30) comment '转股价值',
	price varchar(30) comment '收盘价',
	volume varchar(30) comment '成交额',
	stock_volume varchar(30) comment 'xxx',
	curr_iss_amt varchar(30) comment '剩余规模',
	amt_change varchar(30) comment '',
	turnover_rt varchar(30) comment '换手率',
	cnt varchar(30) comment '',
	end_dt varchar(30) comment '',
	skip_dt varchar(30) comment '',
	start_dt varchar(30) comment '',
	type varchar(30) comment '',
	create_time timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
	update_time timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次修改时间'
)
;

alter table convert_bond_daily add column last_5d_rt varchar(30);
alter table convert_bond_daily add column last_20d_rt varchar(30);
alter table convert_bond_daily add column last_3m_rt varchar(30);
alter table convert_bond_daily add column last_1y_rt varchar(30);
alter table convert_bond_daily add column roe varchar(30);
alter table convert_bond_daily add column dividend_rate varchar(30);
alter table convert_bond_daily add column pe_temperature varchar(30);
alter table convert_bond_daily add column pb_temperature varchar(30);
alter table convert_bond_daily add column int_debt_rate varchar(30);
alter table convert_bond_daily add column pledge_rt varchar(30);
alter table convert_bond_daily add column market_value varchar(30);
alter table convert_bond_daily add column revenue varchar(30);
alter table convert_bond_daily add column revenue_growth varchar(30);
alter table convert_bond_daily add column profit varchar(30);
alter table convert_bond_daily add column profit_growth varchar(30);
alter table convert_bond_daily add column bond_premium_rt varchar(30);
alter table convert_bond_daily add column adjust_condition varchar(30);
alter table convert_bond_daily add column sw_nm_r varchar(30);
alter table convert_bond_daily add column volatility_rate varchar(30);
alter table convert_bond_daily add column convert_amt_ratio2 varchar(30);
alter table convert_bond_daily add column ytm_rt_tax varchar(30);
alter table convert_bond_daily add column pct_rpt varchar(30);
alter table convert_bond_daily add column total_market_value varchar(30);
alter table convert_bond_daily add column redeem_price_total varchar(30);
alter table convert_bond_daily add column redeem_status varchar(30);
alter table convert_bond_daily add column province varchar(30);
alter table convert_bond_daily add column sturnover_rt varchar(30);
alter table convert_bond_daily add column pct_chg varchar(30);
alter table convert_bond_daily add column adjust_status varchar(30);
alter table convert_bond_daily add column unadj_cnt varchar(30);



ALTER TABLE convert_bond_history ADD INDEX idx_date(date);
ALTER TABLE convert_bond_history ADD INDEX idx_bond_id(bond_id);
ALTER TABLE convert_bond_daily ADD INDEX idx_date(date);
ALTER TABLE convert_bond_daily ADD INDEX idx_bond_id(bond_id);



