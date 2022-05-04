from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

MYSQL_USER = os.environ.get('mysql_username')
MYSQL_PASS = os.environ.get('mysql_pass')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e32ba34b72b9afd6b35991afeadfeee717718aa191e6cded584fd0a60d7766c2'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USER}:{MYSQL_PASS}@server/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

from flask_market import routes