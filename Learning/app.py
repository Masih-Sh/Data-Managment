from flask import Flask
import datetime

app = Flask(__name__)


@app.route("/")  # register the / URL with the web server.
def index():
    return datetime.datetime.now().ctime()  # the HTTP response


@app.route("/hello")
def hello():
    return "Hello from my first webapp"


if __name__ == "__main__":
    app.run()
