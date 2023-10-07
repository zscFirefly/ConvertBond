from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://convert_bond:Aa123456@43.143.142.50/convert_bond'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)