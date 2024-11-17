import json
import os
from flask import Flask, jsonify, redirect,render_template, request
from sklearn.model_selection import StratifiedShuffleSplit

from config.config import config


app = Flask(__name__)

journal_path = os.path.join("sessions", "dev", "journal.json")
with open(journal_path, "r") as journal_file:
    JOURNAL = json.load(journal_file)


@app.route("/")
def home():

    return redirect("/log_journal")

@app.route("/log_journal")
def log_journal():

    return render_template("log_journal.html")

@app.route("/new_session")
def new_session():

    return render_template("new_session.html")

@app.route("/get_journal")
def get_journal():

    return jsonify(JOURNAL)



@app.route("/process_resume", methods=["POST"])  # Use methods argument for HTTP methods
def process_resume():
    # Access JSON data sent in the request body
    data = request.json

    # Extract specific fields from the JSON payload
    session_id = data.get("session")
    content = data.get("content")

    # Do some processing (stuff) here

    # Return JSON response with URL and session ID
    return jsonify({'url': 'log_journal', 'session_id': session_id})
