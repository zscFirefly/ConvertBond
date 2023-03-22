from flask import Flask, request, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # 获取用户输入的城市名称
    city = request.form['city']
    
    # 从CSV文件中读取数据
    data = pd.read_csv('data.csv')
    print(data)
    
    # 根据城市名称筛选数据
    results = data[data['city'] == city]

    # 将结果转换为HTML表格
    table = results.to_html(index=False)
    
    # 渲染结果页面
    return render_template('results.html', table=table)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True)
