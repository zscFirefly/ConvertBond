# ConvertBond
可转债爬虫项目


## 目录结构
- **ConvertBondSpider：** 可转债数据爬虫代码、飞书监控代码
  - **run_daily.py** 每日爬可转债数据代码入口
  - **run_history.py** 获取历史所有可转债数据代码
  - **monitor_daily.py** 日常监控可转债信息代码入口
- **etl_scirpt：** ETL数据处理脚本【为后期数仓准备】
- **opt：** 小工具文件夹，一个sql-etl的命令脚本。【为后期数仓准备】
- **script：** 项目初始化数据库脚本

## 环境准备
```shell
pip3 install -r requirements.txt
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



## 备份笔记
git config --global --unset http.proxy # 取消git代理
git config --global --unset https.proxy # 取消git代理
git config --global http.postBuffer 50M # 取消git带宽
