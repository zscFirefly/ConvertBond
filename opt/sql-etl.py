import argparse
import pymysql 
import os

class sqlConfig:
    db_name = ""           # 数据库名
    db_user = "root"              # 用户名
    db_host = "43.143.142.50"         # IP地址
    db_port = 3307                # 端口号
    db_passwd = "Aa123456"            # 密码

def wash_sql(sql_str):
	sql_list = sql_str.split(";")
	sql_list = [x.strip()+";" for x in sql_list if x.strip() != '']
	return sql_list

def read_sql(filename):
	path = os.getcwd()
	filepath = path + '/' + filename
	try:
		with open(filepath,'r') as f:
			sql = f.read()
		return sql
	except FileNotFoundError as e:
		print("ERROR: Not File: " + filepath)
		exit(1)

def get_sql():
	sql_list = []
	parser = argparse.ArgumentParser(description='argparse testing')
	parser.add_argument('--file','-f',type=str, default="-",required=False,help="a sql file")
	parser.add_argument('--edit','-e',type=str, default="-",required=False,help='a sql')
	args = parser.parse_args()
	if args.file == '-' and args.edit == '-':
		print("usage: parse.py [-h] --file FILE --edit EDIT")
		exit()
	if args.file != '-':
		sql_str = read_sql(args.file)
		sql_list += wash_sql(sql_str)
	if args.edit != '-':
		sql_list += wash_sql(args.edit)
	return sql_list


def executor(sql):
    db = pymysql.connect(host=sqlConfig.db_host,port=sqlConfig.db_port,user=sqlConfig.db_user,password=sqlConfig.db_passwd,database=sqlConfig.db_name)     
    cursor = db.cursor()
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    db.close()
    # try:
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     print(results)
    # except pymysql.Error as e:
    #     print("Error: unable to execute")
    # finally:
    #     db.close()
    pass


def main():
	sql_list = get_sql()
	for sql in sql_list:
		executor(sql)

if __name__ == '__main__':
	main()