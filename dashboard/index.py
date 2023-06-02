from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, this will be the dashboard!</p>"

    