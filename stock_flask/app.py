# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
# from model import Stock

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://convert_bond:Aa123456@43.143.142.50/convert_bond'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# # from databases import db

# app = Flask(__name__)


# @app.route('/stocks', methods=['GET'])
# def get_stocks():
#     symbol = request.args.get('symbol')
#     date = request.args.get('date')
#     sort_field = request.args.get('sort_field', 'id')
#     sort_order = request.args.get('sort_order', 'asc')

#     query = Stock.query

#     if symbol:
#         query = query.filter(Stock.symbol == symbol)
#     if date:
#         query = query.filter(Stock.date == date)

#     if sort_field:
#         if sort_order == 'asc':
#             query = query.order_by(getattr(Stock, sort_field).asc())
#         else:
#             query = query.order_by(getattr(Stock, sort_field).desc())

#     stocks = query.all()

#     return {
#         'stocks': [str(stock) for stock in stocks]
#     }



# if __name__ == '__main__':
#     # app.run(debug=True)
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import pymysql

# app = Flask(__name__)

# # 连接MySQL数据库
# conn = pymysql.connect(host='43.143.142.50',port=3307, user='root', password='Aa123456', db='convert_bond')
# cursor = conn.cursor()

# @app.route('/api/data', methods=['POST'])
# def get_data():
#     # 获取请求中的数据
#     data = request.get_json()

#     # 构建SQL查询语句
#     sql = "SELECT * FROM stock_dwd_stock_date"
#     if 'symbol' in data and 'date' in data:
#         sql += f" WHERE symbol='{data['symbol']}' AND date='{data['date']}'"
#     if 'sort_field' in data and 'sort_order' in data:
#         sql += f" ORDER BY {data['sort_field']} {data['sort_order']}"

#     # 执行SQL查询
#     cursor.execute(sql)
#     results = cursor.fetchall()

#     # 将结果转换为JSON格式并返回
#     return jsonify(results)

# @app.teardown_appcontext
# def close_connection(exception):
#     conn.close()

# if __name__ == '__main__':
#     app.run()

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/data', methods=['get', 'post'])
def get_data():
    # 获取URL中的参数，例：http://127.0.0.1:5000/data?page=1&limit=10，获取?后的数据
    print('URL中的参数：%s' % request.args)
    # 获取表单数据,即Content-Type为multipart/form-data的数据
    print('表单数据：%s' % request.form)
    # 获取Content-Type为application/json的数据
    print('application/json的数据：%s' % request.json)
    # 获取Content-Type为text/plain的数据
    print('text/plain的数据：%s' % request.data)
    # 获取请求头
    print('请求头：%s' % request.headers)
    # 获取请求路径
    print('请求路径：%s' % request.path)
    # 获取user_agent
    print('user_agent：%s' % request.user_agent)
    # 获取请求地址
    print('请求地址：%s' % request.url)
    # 获取Cookies
    print('Cookies：%s' % request.cookies)
    # 获取认证数据
    print('认证数据：%s' % request.authorization)
    # 获取上传文件
    print('上传文件：%s' % request.files)
    # jsonify可返回list, dict等格式的数据
    return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8000)

