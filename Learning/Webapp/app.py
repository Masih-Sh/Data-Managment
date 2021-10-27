from flask import Flask, request, render_template
import datetime

app = Flask(__name__)


@app.route("/")  # resigter the / URL with the Flask web server
def index():
    return datetime.datetime.now().ctime()  # the HTTP responce


@app.route("/hello")
def hello():
    return "Hello I finally understand what is going on here!"

@app.get("/home")
def home_page():
        return render_template("home.html")    


@app.get("/showform")
def display_form():
    return render_template("form.html")

@app.post("/processform")
def process_form():
    the_name = request.form["thename"]
    the_dob = request.form["thedob"]
    with open("suckers.text", "a") as sf:
        print(f"{the_name}, {the_dob}", file=sf)
    return f"Hi there , {the_name} , we know you were born on : {the_dob} ."
    

if __name__ == "__main__":
    app.run(debug=True)