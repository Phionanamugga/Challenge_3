from flask import Flask
from api.views import incident, user

app = Flask(__name__)
app.register_blueprint(incident)
app.register_blueprint(user)

