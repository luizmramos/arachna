from flask import Flask
from flask import render_template
from flask import request
from dbmanager import get_all_by_score
from dbmanager import get_all_by_problems
from dbmanager import get_amount
from dbmanager import get_all
from dbmanager import copy

app = Flask(__name__)

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
def index(page=1):
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        user = request.form["user"]
        users = convert(get_all(), 1)
        amount = len(users)
        filtered = filter(lambda u: u["username"] == user, users)
        
        if filtered:
            rank = filtered[0]["rank"]
            page = (rank-1) / 1000 + 1
        else:
            rank = -1
            page = 1

        users_list = get_all_by_score(page)
        template = render_template("search.html", users=convert(users_list, page), amount=amount, page=page, rank=rank)
    except Exception as e:
        print e
    return template

@app.route("/score/")
@app.route("/score/<int:page>")
def score(page=1):
    try:
        amount = get_amount()
        users_list = get_all_by_score(page if page <= amount else amount)
        template = render_template("rank.html", users=convert(users_list, page), amount=amount, page=page)
    except Exception as e:
        print e
    return template

@app.route("/problems/")
@app.route("/problems/<int:page>")
def problems(page=1):
    try:
        amount = get_amount()
        users_list = get_all_by_problems(page if page <= amount else amount)
        template = render_template("rank.html", users=convert(users_list, page), amount=amount, page=page)
    except Exception as e:
        print e
    return template

if __name__ == "__main__":
    copy()
    app.run(host="0.0.0.0")

