from api import app


@app.route('/')
def index():
    return jsonify({"message": "Welcome to ireporter application"})


if __name__ == '__main__':
    app.run(debug=True)
