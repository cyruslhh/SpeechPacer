import math
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import csv
import random
from google.cloud import speech
import io
import Levenshtein

from helpers import login_required

# Configure application (Configs taken from C$50 Finance)
app = Flask(__name__)

# Ensure templates are auto-reloaded (Configs taken from C$50 Finance)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached (Configs taken from C$50 Finance)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies) (Configs taken from C$50 Finance)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Start database connection to SpeechPacer database
db = SQL("sqlite:///SpeechPacer.db")

@app.route("/")
def index():
    '''Home page, which just shows some general information about the website'''
    #check if user is logged in, and change navbar display accordingly.
    if session.get("user_id") is not None:
        rows = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = rows[0]["username"]
        return render_template("index.html", logged=True, username=name)
    return render_template("index.html", logged=False)


@app.route("/logout")
def logout():
    '''Logs the user out'''
    session.clear()
    return redirect("/")

@app.route("/login", methods=["POST", "GET"])
def login():
    '''Logs the user in'''
    if request.method == "GET":
        #Just returns template for registering new account
        return render_template("login.html")
    if request.method == "POST":
        #Logs the user in, redirected from login.html.
        username = request.form.get("username")
        password = request.form.get("password")

        #check if username and password were filled in
        if not username:
            return render_template("error.html", message="Please input a username!")
        if not password:
            return render_template("error.html", message="Please input a password!")

        #check if username exists
        rows = db.execute("SELECT * FROM users WHERE username=?", username)
        if(len(rows) == 0):
            return render_template("error.html", message="Invalid username!")

        #check if the passwords match
        if( not check_password_hash(rows[0]["password"], password)):
            return render_template("error.html", message="Wrong password!")

        #set session's user_id to logged in id.
        session["user_id"] = rows[0]["id"]

        #return template with logged in navbar.
        return render_template("index.html", logged=True, username=username)

@app.route("/exercises", methods=["POST", "GET"])
@login_required
def exercise():
    '''Page where user will be doing exercises. '''
    if request.method == "GET":
        #Create 2 empty lists for the words to be spoken.
        sample_text = []
        actual_text = []

        #open the text file full of grade 5 level words
        with open('Grade5Words.txt') as textfile:
            #read lines and choose, without repeats, 40 words from the text file. Assign to the two lists, 20 words each.
            texts = textfile.readlines()
            chosen_texts = random.sample(texts, 40);
            for i in range(0, 20):
                sample_text.append(chosen_texts[i].strip())
                actual_text.append(chosen_texts[i + 20].strip())

        #Get the currently logged in user's speed.
        speedRow = db.execute("SELECT speed FROM speed WHERE user_id=?", session["user_id"])
        if (len(speedRow) == 0):
            db.execute("INSERT INTO speed (user_id, speed) VALUES (?, ?)", session["user_id"], 50)
            speedRow = db.execute("SELECT speed FROM speed WHERE user_id=?", session["user_id"])
        speed = speedRow[0]["speed"]

        #Get the currently logged in user's username. Render template with all this information.
        username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
        return render_template("exercise.html", sample=sample_text, text=actual_text, speed=speed, username=username)
    if request.method == "POST":
        #Redirected after exercise is finished. Updates a user's speed to the passed in parameter.
        db.execute("UPDATE speed SET speed=? WHERE user_id=?", round(float(request.form.get("speed")), 2), session["user_id"])
        return redirect('/exercises')

@app.route("/register", methods=["POST", "GET"])
def register():
    '''Registers a new user'''
    if request.method == "GET":
        return render_template("register.html");
    if request.method == "POST":
        #Registers a new user, and then redirects to the login page
        username = request.form.get("username")
        password = request.form.get("password")

        #check if username and password were filled in
        if not username:
            return render_template("error.html", message="Please input a username!")
        if not password:
            return render_template("error.html", message="Please input a password!")

        #Check if username was already taken
        rows = db.execute("SELECT * FROM users WHERE username=?", username)
        if(len(rows) != 0):
            return render_template("error.html", message="That username is already taken!")

        #Insert into users, and then show login.html for them to log in.
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, generate_password_hash(password))
        return render_template("login.html")

@app.route("/score", methods=["POST", "GET"])
def score():
    return "test"


def score_speech(speech_file, target_time, target_words):
    '''scores the speech file in a scale from 0-100 (100 being perfect) for timing and target_words'''
    time_off, accuracy_off = get_time_and_levenshtein(speech_file, target_time, target_words)
    word_score = round(s_curve(target_words))
    time_score = round(s_curve(time_off*100))
    return word_score, time_score

def transcribe_file(speech_file):
    """Transcribe the given audio file. Returns a list of transcribed words and their timestamps"""

    client = speech.SpeechClient()


    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)
    output = []
    # Each result is for a consecutive portion of the audio. Iterate through
    for result in response.results:
        alternative = result.alternatives[0]
        for word in alternative.words:
            word.start_time = (word.start_time["seconds"] + word.start_time["nanos"] * 10**-9) * 1000
            word.end_time = (word.end_time["seconds"] + word.end_time["nanos"] * 10**-9) * 1000
            output.append(word)
    return output
    
def s_curve(x):
    '''S curve with roughly 50 at x=10, 100 for x <= 0, and 0 for x >= 40'''
    return 100 - (100/(1+(math.exp(-0.25*x)))**10)

def get_time_and_levenshtein(speech_file, target_time, target_words):
    '''returns how off the speech_file is from the target words and target time between words, in milliseconds'''
    word_infos = transcribe_file(speech_file)
    total_time_off = 0
    total_levenshtein_distance_off = 0
    for i in range(len(word_infos)):
        word_info = word_infos[i]
        previous_info = word_infos[i - 1]

        if (i != 0):
            time_off = math.abs(target_time - (word_info.start_time - previous_info.start_time))
            if (time_off > 49):
                total_time_off += time_off
        
        min_distance = math.inf
        for target in target_words:
            distance = Levenshtein.distance(word_info.word, target)
            if (min_distance > distance):
                min_distance = distance
        total_levenshtein_distance_off = min_distance
    return total_time_off, total_levenshtein_distance_off