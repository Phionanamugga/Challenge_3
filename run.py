from api import app
from flask import jsonify

@app.route('/')
def index():
    return jsonify({"message": "Welcome to ireporter application"})


if __name__ == '__main__':
    app.run()
