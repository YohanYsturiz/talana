import json
import random

from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/kombat/start")
def kombat_start():
    return "Start Fight"


if __name__ == "__main__":
    app.run()
