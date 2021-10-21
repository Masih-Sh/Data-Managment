from flask import Flask , request
import datetime

app = Flask(__name__)


@app.route("/")  # register the / URL with the web server.
def index():
    return datetime.datetime.now().ctime()  # the HTTP response


@app.route("/hello")
def hello():
    return "Hello from my first webapp"


@app.get("/showform")
def display_form():   
    return html

@app.post("/processform")
def process_form():
    the_name = request.form["thename"]
    the_dob = request.form["thedob"]
    with open("sucker.txt" , "a") as sf:
        print(f"{the_name} ,{the_dob}" , file=sf)
    return f"Hi there, {the_name} , we know you were born on : {the_dob}."

if __name__ == "__main__":
    app.run(debug=True)
