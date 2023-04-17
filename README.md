# ConvertBond
## 简述
实现可转债/ETF基金爬虫项目，用于可抓债与ETF基金的爬虫，同时根据常见的量化策略：可转载双低轮动策略及ETF基金MACD金叉策略，挖掘市场中存在的一些投资机会，如有道友，欢迎交流～


## 目录结构
- **ConvertBondSpider：** 可转债数据爬虫代码、飞书/企微监控代码
  - **bin** 可执行py文件
    - **change_daily.py** 可转债交易提醒代码
    - **run_daily.py** 每日爬可转债数据代码入口
    - **run_history.py** 获取历史所有可转债数据代码
    - **monitor_daily.py** 日常监控可转债信息代码入口
  - **common** 公共方法
    - **calender.py** 日历相关的方法，主要用于判断是否为交易日
    - **feishu.py** 飞书公共方法，主要实现飞书的消息推送
    - **search_data.py** 数据库链接的相关方法，查数，写数基于此方法
    - **wechat.py** 企业微信公共方法，主要实现企业微信应用的推送
  - **conf** 配置类
    - **feishu_config.py** 飞书的配置类
    - **sql_config.py** mysql数据库的配置类
    - **wechat_config.py** 企业微信的配置类
  - **core** 业务代码
    - **account.py** 可转债回测的核心代码
    - **monitor.py** 监控相关的代码
    - **script_config.py** 集思录登陆验证类
    - **script_etf_config.py** 雪球核心配置代码
    - **scripy_convert_bond.py** 可转债爬虫核心代码
    - **scripy_etf_fund.py** ETF爬虫核心代码
    - **user_login.py** 可转债登陆核心代码
- **etl_scirpt：** ETL数据处理脚本【为后期数仓准备】
- **opt：** 小工具文件夹，一个sql-etl的命令脚本。【为后期数仓准备】
- **script：** 项目初始化数据库脚本

## 环境准备
```shell
pip3 install -r requirements.txt
```
liunx安装ta-lib库
```shell
# 获取源码库
sudo wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
# 解压进入目录
tar -zxvf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
# 编译安装
sudo ./configure --prefix=/usr  
sudo make
sudo make install
# 重新安装python的TA-Lib库
pip install TA-Lib==0.4.16
# 或者不带版本  pip install TA-Lib
```


## build脚本
```shell
cat << EOF >>  ~/.bash_profile
JOB_HOME="/root/job/ConvertBond/opt"
PATH=\$PATH:\$JOB_HOME
export \$PATH
EOF

source ~/.bash_profile

ln -s sql-etl.sh sql-etl
```

## 项目难点
1. 集思录登陆：调用登陆接口，换取session后，需要调用主页接口才能激活session，用session去调用可转债列表数据。
2. 飞书调用群消息接口：需要创建应用，启动机器人，获取用户id。参考链接：https://blog.csdn.net/viviliving/article/details/121589128
3. 企业微信应用消息的推送。实现方式参考链接：https://blog.csdn.net/weixin_44505713/article/details/130177269?utm_source%20=%20uc_fansmsg

## 备份笔记
git config --global --unset http.proxy # 取消git代理
git config --global --unset https.proxy # 取消git代理
git config --global http.postBuffer 50M # 取消git带宽
git config core.ignorecase false # 取消大小写敏感

