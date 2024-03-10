from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ecf2251cb4208b6da7ffb8cb4058f939'

from system import routes