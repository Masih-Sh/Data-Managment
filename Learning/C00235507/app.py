from flask import Flask, render_template

app = Flask(__name__)



@app.get("/home")
def home_page():
    return render_template("home.html", the_title="Welcome!")


@app.get("/personalinfo")
def personal_page():
    return render_template("personal.html", the_title="Personal Info :")

@app.get("/cvinfo")
def cv_page():
    return render_template("cv.html", the_title="My CV :")

@app.get("/gamesinfo")
def games_page():
    return render_template("games.html", the_title="My Favorite Games:")

@app.get("/rdr1&2info")
def rdr_page():
    return render_template("rdr1&2.html", the_title="Red Dead redemption 1&2:")

@app.get("/gtainfo")
def gta_page():
    return render_template("gta.html", the_title="Grand Theft Auto :")

@app.get("/bullyinfo")
def bully_page():
    return render_template("bully.html", the_title="Bully Game :")

@app.get("/intrestsinfo")
def intrest_page():
    return render_template("intrest.html", the_title="My Intrests :")

if __name__ == "__main__":
    app.run(debug=True)
