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







create table dwd_convert_bond_detail_d (
	bond_id int(30) comment 'id',
	`date` date comment '日期', 
	bond_nm varchar(30) comment '可转债名称',
	price decimal(18,4) comment '可转债价格',
	premium_rt decimal(18,4) comment '可转债溢价率',
	ytm_rt decimal(18,4) comment '到期税前收益率',
	curr_iss_amt decimal(30,4) comment '剩余规模',
	volume decimal(30,4) comment '成交额',
	turnover_rt decimal(30,4) comment '换手率',
	convert_value decimal(30,4) comment '转股价值',
	etl_load_time timestamp comment '数据加工时间'
)ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债数据明细表'

;

----------------------------------------------------------
----------------- 以下代码构造日历表 -------------------------
----------------------------------------------------------

CREATE TABLE `dim_date` (  
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_id` varchar(10) DEFAULT NULL,     
  `day_short_desc` varchar(10) DEFAULT NULL,  
  `day_long_desc` varchar(50) DEFAULT NULL,  
  `week_desc` varchar(20) DEFAULT NULL,  
  `week_id` varchar(20) DEFAULT NULL,  
  `week_long_desc` varchar(50) DEFAULT NULL,  
  `month_id` varchar(20) DEFAULT NULL,  
  `month_long_desc` varchar(50) DEFAULT NULL,  
  `quarter_id` varchar(20) DEFAULT NULL,  
  `quarter_long_desc` varchar(20) DEFAULT NULL,  
  `year_id` varchar(20) DEFAULT NULL,  
  `year_long_desc` varchar(50) DEFAULT NULL,  
  PRIMARY KEY (`id`)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE PROCEDURE `f_dim_date`(in yr VARCHAR(20))
begin  
declare i int;
declare start_date varchar(20);
declare end_date varchar(20);
declare date_count int;

    set i=0;  
        set start_date= concat(yr, '-01-01');
        set end_date = concat(yr+1,'-01-01');
    DELETE from dim_date where year_id = yr;
        set date_count = datediff(end_date, start_date);
        
    while i < date_count DO  
        INSERT into dim_date (day_id,day_short_desc,day_long_desc,week_desc,week_id,week_long_desc,month_id,month_long_desc,quarter_id,quarter_long_desc,year_id,year_long_desc)  
            SELECT  
                            DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y%m%d') day_id,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y-%m-%d') day_short_desc,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y年%m月%d日') day_long_desc,  
                case dayOFweek(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'))  when 1 then '星期日' when 2 then '星期一' when 3 then '星期二' when 4 then '星期三' when 5 then '星期四' when 6 then '星期五' when 7 then '星期六' end week_desc,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y%u') week_id,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y年第%u周') week_long_desc,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y%m') month_id,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y年第%m月') month_long_desc,  
                CONCAT(DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y'),quarter(STR_TO_DATE( start_date,'%Y-%m-%d %H:%i:%s'))) quarter_id,  
                CONCAT(DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y'),'年第',quarter(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s')),'季度') quarter_long_desc,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y') year_id,  
                DATE_FORMAT(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),'%Y年') year_long_desc  
        from dual;  
        set i=i+1;  
        set start_date = DATE_FORMAT(date_add(STR_TO_DATE(start_date,'%Y-%m-%d %H:%i:%s'),interval 1 day),'%Y-%m-%d');  
    end while;  
end
;

call f_dim_date('2013');
call f_dim_date('2014');
call f_dim_date('2015');
call f_dim_date('2016');
call f_dim_date('2017');
call f_dim_date('2018');
call f_dim_date('2019');
call f_dim_date('2020');
call f_dim_date('2021');
call f_dim_date('2022');
call f_dim_date('2023');

alter table `dim_date` add column is_work tinyint;
alter table `dim_date` add column is_holiday tinyint;
alter table `dim_date` add column is_caculate tinyint;

alter table `dim_date` add column is_change tinyint;


update dim_date set is_holiday=0;
update dim_date set is_holiday=1
where day_short_desc in ('2022-01-01','2022-01-02','2022-01-03','2022-01-31','2022-02-01','2022-02-02'
    ,'2022-02-03','2022-02-04','2022-02-05','2022-02-06','2022-04-03','2022-04-04','2022-04-05'
    ,'2022-04-30','2022-05-01','2022-05-02','2022-05-03','2022-05-04','2022-06-03','2022-06-04'
    ,'2022-06-05','2022-09-10','2022-09-11','2022-09-12','2022-10-01','2022-10-02','2022-10-03'
    ,'2022-10-04','2022-10-05','2022-10-06','2022-10-07');
update dim_date set is_work=1 where week_desc in ('星期一','星期二','星期三','星期四','星期五') and is_holiday = 0;
update dim_date set is_work=0 where week_desc in ('星期六','星期日') or is_holiday=1;




update dim_date set is_work = 0 where day_id in ('20210101','20210102','20210103','20210211','20210212','20210213','20210214','20210215','20210216','20210217','20210403','20210404','20210405','20210501','20210502','20210503','20210504','20210505','20210612','20210613','','20210614','20210919','20210920','20210921','20211001','20211002','20211003','20211004','20211005','20211006','20211007')


create table convert_bond_loopback (
  bond_id int(30) comment 'id',
  `date` date comment '日期', 
  ytm_rt varchar(30) comment '到期税前收益率',
  premium_rt varchar(30) comment '转股溢价率',
  price varchar(30) comment '收盘价',
  rn int comment '序列号',
  create_time timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次修改时间'
)
;




ALTER TABLE convert_bond_loopback ADD INDEX idx_date(date);
ALTER TABLE convert_bond_loopback ADD INDEX idx_bond_id(bond_id);




select bond_id,max(date) convert_bond_total
group by bond_id

-- 清洗数据


CREATE TABLE `convert_bond_total` (
  bond_id int(30) DEFAULT NULL COMMENT '转债ID',
  date date DEFAULT NULL COMMENT '日期',
  ytm_rt varchar(30) DEFAULT NULL COMMENT '到期税前收益率',
  premium_rt varchar(30) DEFAULT NULL COMMENT '溢价率',
  price  varchar(30) DEFAULT NULL COMMENT '价格',
  convert_value varchar(30) DEFAULT NULL COMMENT '转债价值',
  turnover_rt varchar(30) DEFAULT NULL COMMENT '换手率',
  volume varchar(30) DEFAULT NULL COMMENT '成交额',
  curr_iss_amt  varchar(30) DEFAULT NULL COMMENT '剩余规模'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债汇总数据(手动触发)'
;

CREATE TABLE `convert_bond_total_prod` (
  bond_id int(30) DEFAULT NULL COMMENT '转债ID',
  date date DEFAULT NULL COMMENT '日期',
  ytm_rt varchar(30) DEFAULT NULL COMMENT '到期税前收益率',
  premium_rt varchar(30) DEFAULT NULL COMMENT '溢价率',
  price  varchar(30) DEFAULT NULL COMMENT '价格',
  convert_value varchar(30) DEFAULT NULL COMMENT '转债价值',
  turnover_rt varchar(30) DEFAULT NULL COMMENT '换手率',
  volume varchar(30) DEFAULT NULL COMMENT '成交额',
  curr_iss_amt  varchar(30) DEFAULT NULL COMMENT '剩余规模'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债汇总数据(手动触发)'
;


-- 近5年的可转债数据。
insert into convert_bond_total
-- 日常数据
select bond_id
, date
, ytm_rt
, premium_rt
, cast(price as Decimal(30,2)) as price
, convert_value
, turnover_rt
, volume
, cast(curr_iss_amt as Decimal(30,2)) as curr_iss_amt
from convert_bond_daily
-- union 
-- -- 所有0320问题，丢失数据
-- select bond_id
-- , date
-- , ytm_rt
-- , premium_rt
-- , cast(price as Decimal(30,2)) as price
-- , convert_value
-- , turnover_rt
-- , volume
-- , cast(curr_iss_amt as Decimal(30,2)) as curr_iss_amt
-- from tmp_convert_bond_history_0320
-- where date = '2023-03-10'
union 
-- 所有0402问题，丢失数据
select bond_id
, date
, ytm_rt
, premium_rt
, cast(price as Decimal(30,2)) as price
, convert_value
, turnover_rt
, volume
, cast(curr_iss_amt as Decimal(30,2)) as curr_iss_amt
from tmp_convert_bond_history_0402
where date in ('2023-03-29','2023-03-30','2023-03-10')
union 
-- 所有历史数据
select bond_id
, date
, ytm_rt
, premium_rt
, cast(price as Decimal(30,2)) as price
, convert_value
, turnover_rt
, volume
, cast(curr_iss_amt as Decimal(30,2)) as curr_iss_amt
from  tmp_convert_bond_history
where date between '2018-01-01' and '2023-12-31'
