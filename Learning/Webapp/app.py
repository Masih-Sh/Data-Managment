
from flask import Flask

import datetime

app = Flask(__name__)


@app.route("/")  #resigter the / URL with the Flask web server
def index():
    return datetime.datetime.now().ctime()      #the HTTP responce

@app.route("/hello")
def hello():
    return "Hello I finally understand what is going on here!"

if __name__ =="__main__":
    app.run() 