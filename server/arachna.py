#!/usr/bin/python

import logging
import signal
import sys
from dbmanager import copy, get_all, get_all_by, get_amount
from flask import Flask, render_template, request
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
handler = TimedRotatingFileHandler("/Arachna/logs/server/log", when="midnight", backupCount=7)
logger = logging.getLogger('werkzeug')

logger.setLevel(logging.INFO)
logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

def convert(users_list, page):
    return [
        {
            'rank': rank+1+1000*(page-1),
            'username': user[0],
            'problems': user[1],
            'score': user[2]
        }
        for rank, user in enumerate(users_list)
    ]

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", url="index")

@app.route("/search/<type>", methods=["POST"])
def search(type):
    if not (type == "score" or type == "problems"):
        type = "score"

    user = request.form["user"]
    users = convert(get_all(type), 1)
    amount = get_amount()
    filtered = filter(lambda u: u["username"] == user, users)
    
    if filtered:
        rank = filtered[0]["rank"]
        page = (rank-1) / 1000 + 1
    else:
        rank = -1
        page = 1

    users_list = get_all_by(type, page)
    return render_template("search.html", users=convert(users_list, page), amount=amount, page=page, rank=rank, url=type)

@app.route("/score/")
@app.route("/score/<int:page>")
def score(page=1):
    amount = get_amount()
    page = page if page <= amount else amount
    users_list = get_all_by("score", page)
    return render_template("rank.html", users=convert(users_list, page), amount=amount, page=page, url="score")

@app.route("/problems/")
@app.route("/problems/<int:page>")
def problems(page=1):
    amount = get_amount()
    page = page if page <= amount else amount
    users_list = get_all_by("problems", page)
    return render_template("rank.html", users=convert(users_list, page), amount=amount, page=page, url="problems")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

def signal_handler(signal, frame):
    logger.warn("=== Process stopped (%d) ===" % signal)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    copy()
    app.run(host="0.0.0.0", port=80)

