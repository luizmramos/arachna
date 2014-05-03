from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    users = [
        {
            "rank": 1,
            "username": 'vyrp',
            "problems": 100,
            "score": 40.30,
        },
        {
            "rank": 2,
            "username": 'harry',
            "problems": 90,
            "score": 35.35,
        },
        {
            "rank": 3,
            "username": 'h4x0r',
            "problems": 85,
            "score": 33.67,
        },
    ]
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

