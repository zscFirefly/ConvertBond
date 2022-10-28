# ConvertBond
可转债爬虫项目


## 环境准备
pip3 install -r requirements.txt

## build脚本
```shell
cat << EOF >>  ~/.bash_profile
JOB_HOME="/root/job/ConvertBond/opt"
PATH=\$PATH:\$JOB_HOME
export \$PATH
EOF

source ~/.bash_profile
```
ln -s sql-etl.sh sql-etl



## 日常跑批
python3 runDaily.py

## 历史数据初始化
python3 runHistory.py


## 备份笔记
git config --global --unset http.proxy # 取消git代理
git config --global --unset https.proxy # 取消git代理
git config --global http.postBuffer 50M # 取消git带宽
