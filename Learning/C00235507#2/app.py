from flask import Flask, render_template, request, session
import random
from flask_session import Session
from collections import Counter
from datetime import datetime, timedelta
import DBcm
import socket


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

bigWordList = []
smallWordList = []
w = []
randomWord = ""

allWords = open("word.txt", "r")
for words in allWords:
    words = words.lower().strip()
    if "'s" in words:
        continue
    if len(words) <= 3:
        continue
    if len(words) >= 8:
        bigWordList.append(words)
    else:
        smallWordList.append(words)

config = {
    "host": "127.0.0.1",
    "database": "project2_db",
    "user": "project2",
    "password": "project2password",
}


def save_the_data(time, name, sourceword, userinput):
    SQL = """
        insert into players
        (time,name,sourceword,userinput) values (%s,%s,%s,%s)
    """
    with DBcm.UseDatabase(config) as db:
        db.execute(SQL, (time, name, sourceword, userinput))


def save_the_log(result, sourceword, userinput, ip, explorer):
    SQL = """
        insert into logs
        (result,sourceword,userinput,ip,explorer) values (%s,%s,%s,%s,%s)
    """
    with DBcm.UseDatabase(config) as db:
        db.execute(SQL, (result, sourceword, userinput, ip, explorer))


def process_data():
    with DBcm.UseDatabase(config) as db:
        SQL = """
          select time, name, sourceword, userinput
          from players
          order by time
        """
        db.execute(SQL)
        scores = db.fetchall()

        while len(scores) < 10:
            scores.append([])

    return scores[:10]


def process_logs():
    with DBcm.UseDatabase(config) as db:
        SQL = """
          select result,sourceword,userinput,time,ip,explorer
          from logs
          order by time desc
        """
        db.execute(SQL)
        logs = db.fetchall()

        while len(logs) <= 0:
            logs.append([])

    return logs


@app.get("/home")
def home_page():
    return render_template("home.html", the_title="Welcome Page")


@app.get("/game")
def game_page():
    randomWord = random.choice(bigWordList)
    session["randomWord"] = randomWord
    startTime = datetime.now()
    session["submitted"] = False
    session["startTime"] = startTime
    return render_template("game.html", the_tile="Game Page", randomWord=randomWord)


@app.post("/result")
def showing_results():
    session["user_input"] = request.form["user_input"]
    userWords = session.get("user_input")
    startTime = session.get("startTime")
    endTime = datetime.now()
    session["endTime"] = datetime.now()

    currentTime = endTime.timestamp() - startTime.timestamp()

    currentTime = round(currentTime, 2)

    session["currentTime"] = currentTime

    randomWord = session.get("randomWord")
    userWords = userWords.lower()
    chunks = userWords.split(" ")
    missSpelledWords = []
    userInputList = []
    invalidLetters = []

    resultString = ""

    result = True

    for x in chunks:
        if x in smallWordList:
            userInputList.append(x)
        else:
            missSpelledWords.append(x)
            result = False

    result1 = ""
    result1 = str(missSpelledWords)
    w = []

    for x in chunks:
        w.append(Counter(x))

    S = Counter(randomWord)
    invalidLetters = []

    for words in w:
        for letters in words:
            if words[letters] > S[letters]:
                invalidLetters.append(letters)
                result = False

    if result == True:
        resultString = "Congradulation!!"
        buttonState = ["none", "block"]
        session["result"] = "!!SUCCES!!"

    else:
        resultString = "Keep on Trying!!"
        buttonState = ["block", "none"]
        session["result"] = "!!FAIL!!"

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    result = session.get("result")
    save_the_log(
        result, randomWord, userWords, IPAddr, request.headers.get("User_Agent")
    )

    return render_template(
        "result.html",
        the_tile="result Page",
        result1=result1,
        randomWord=randomWord,
        invalidLetters=invalidLetters,
        resultString=resultString,
        buttonState=buttonState,
        currentTime=currentTime,
    )


@app.post("/final")
def showing_final_result():
    session["user_name"] = request.form["user_name"]
    user_name = session.get("user_name")
    currentTime = session.get("currentTime")
    sourceWord = session.get("randomWord")
    userWords = session.get("user_input")

    if session.get("submitted") == False:
        save_the_data(currentTime, user_name, sourceWord, userWords)
    scores = []
    scores = process_data()
    session["submitted"] = True
    return render_template("final.html", the_tile="Final Page", scores=scores)


@app.get("/log")
def showing_logs():
    logs = process_logs()
    showingLine = ""
    for x in logs:
        # result
        showingLine += f"{x[0]}" + " : "
        # adding source word
        showingLine += f"{x[1]}" + " - "
        # adding user input and going to next line
        showingLine += f"{x[2]}" + "<br>"
        # adding time
        showingLine += f"{x[3]}" + " - "
        # adding ip
        showingLine += f"{x[4]}" + " - "
        # adding the explorer
        showingLine += f"{x[5]}" + "<br>"
        showingLine += "=================================<br>"

    return render_template("logs.html", the_tile="Log Page", showingLine=showingLine)


if __name__ == "__main__":
    app.run(debug=True)
