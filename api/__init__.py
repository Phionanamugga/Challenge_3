from flask import Flask
from api.views import incident, user
# from flask_jwt_extended import JWTManager


app = Flask(__name__)
# JWTManager(app)
app.register_blueprint(incident)
app.register_blueprint(user)
app.config['JWT_SECRET_KEY'] = 'thisisatopsecretkey'
