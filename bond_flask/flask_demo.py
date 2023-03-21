from flask import Flask, request, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

def get_data(bond_id):

    db_info = {
        'user': 'root',
        'password': 'Aa123456',
        'host': '43.143.142.50',
        'port': 3307,
        'database': 'convert_bond'
    }

    engine = create_engine(
        'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info,
        encoding='utf-8'
    )
    sql = ''' select date,bond_id,bond_nm,price,increase_rt,premium_rt,year_left,ytm_rt from convert_bond_daily where bond_id = '%s' ''' % (bond_id)
    data = pd.read_sql(sql, engine)
    columns={"date": "日期", "bond_id": "转债代码", "bond_nm": "转债名称", "price": "价格", "premium_rt": "溢价率", "year_left": "到期时间", "ytm_rt": "到期税前收益率", "increase_rt": "涨幅"}

    data = data.rename(columns=columns)
    print(data)

    return data


@app.route('/')
def index():
    return render_template('index02.html')

@app.route('/search', methods=['POST'])
def search():
    # 获取用户输入的城市名称
    bond_id = request.form['bond_id']
    
    # 从CSV文件中读取数据
    # data = pd.read_csv('data.csv')
    
    # 根据城市名称筛选数据
    # results = data[data['city'] == city]

    results = get_data(bond_id)
    
    # 将结果转换为HTML表格
    table = results.to_html(index=False)
    
    # 渲染结果页面
    return render_template('results02.html', table=table)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
