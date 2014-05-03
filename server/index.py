from flask import Flask
from flask import render_template
from dbmanager import get_all_by_score

app = Flask(__name__)

def convert(users_list):
    return [
        {
            'rank': rank+1,
            'username': user[0],
            'problems': user[1],
            'score': user[2]
        }
        for rank, user in enumerate(users_list)
    ]

@app.route("/")
def index():
    users = get_all_by_score()
    return render_template("index.html", users=convert(users))

if __name__ == "__main__":
    app.run(host="0.0.0.0")

