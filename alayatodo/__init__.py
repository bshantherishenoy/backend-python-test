from flask import Flask, g
import sqlite3
import os
# configuration
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
print(PROJECT_ROOT)
DATABASE = os.path.join(PROJECT_ROOT, 'tmp', 'alayatodo.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)





def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

import alayatodo.views
