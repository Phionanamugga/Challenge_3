from flask import jsonify, request, abort, Blueprint
from .models import Incident, User
from datetime import datetime, timedelta
from api.models import Incident
import json
from database import DatabaseConnection
from api.validate import check_fields_required, errors
from functools import wraps
import jwt
import re


incident = Blueprint('record', __name__)
user = Blueprint('user', __name__)

errors = {}
text_fields = ['othernames', 'firstname', 'lastname', 'username']
key_fields = ['email', 'password']
name_regex = r"[a-zA-Z]"
password_regex = r"(?=.*[0-9])"
username_regex = r"[a-zA-Z0-9_]"
phone_regex = r"\d{3}-\d{3}-\d{4}"

incident = Blueprint('record', __name__)
new_incident = Incident()                   
new_user = User()
secret_key='thisisatopsecretkey'


def token_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({"message": "Missing Token"}), 403
            jwt.decode(token, secret_key)
        return f(*args, **kwargs)
    return decorated


@incident.route('/api/v2/interventions', methods=['POST'])
@token_required
def create_incident():
    data = request.get_json()
    created_incident = new_incident.add_incident(data)
    return jsonify({"message": " Successfully created",
                    "intervention": created_incident}), 200


@incident.route('/api/v2/interventions', methods=['GET'])
@token_required
def fetch_incident():
    # fetches all user's incidents
    fetched_incidents = new_incident.get_incident()
    return jsonify({'incidents': fetched_incidents, 'status':'200'}), 200


@incident.route('/api/v2/interventions/<int:incident_id>', methods=['GET'])
@token_required
def fetch_single_incident(incident_id):
    fetched_incident = []
    fetched_incident = new_incident.fetch_single_incident(incident_id)
    return jsonify({"incident": fetched_incident})

@incident.route('/api/v2/interventions/<int:incident_id>', methods=['DELETE'])
@token_required
def delete_incident(incident_id):
    # this function enables user delete incident
    if incident_id == 0:
        return jsonify({"message": "This record doesnot exist", 'status': '400'}), 400
    new_incident.delete_incident(incident_id)
    return jsonify({"message": "incident successfully deleted"}), 200


@incident.route('/api/v2/redflag/<int:incident_id>/status', methods=['PATCH'])
@token_required
def edit_redflag_status(incident_id):
    # This method updates a incident
    user = User()
    data = request.get_json()
    new_incident.update_incident(data['status'], incident_id)
    return jsonify({"status": 200,
                    "data": "successfully edited"}), 200


@incident.route('/api/v2/interventions/<int:incident_id>/location', methods=['PATCH'])
@token_required
def edit_intervention_location(incident_id):
    # This method updates a incident
    data = request.get_json()
    # if admin = True:
    print(data, incident_id)
    new_incident.update_incident(data['location'], incident_id)
    return jsonify({"status": 200,
                    "data": "Updated intervention record's location"}), 200


@incident.route('/api/v2/interventions/<int:incident_id>/comment', methods=['PATCH'])
@token_required
def edit_intervention_comment(incident_id):
    # This method updates a incident
    data = request.get_json()
    # if admin = True:
    new_incident.update_incident(data['comment'], incident_id)
    return jsonify({"status": 200,
                    "data": "Updated intervention record's comment"}), 200


@incident.route('/api/v2/interventions/<int:incident_id>/status', methods=['PATCH'])
@token_required
def edit_intervention_status(incident_id):
    # This method updates a incident
    data = request.get_json()
    # if admin = True:
    new_incident.update_incident(data['status'], incident_id)
    return jsonify({"status": 200,
                    "data": "Updated red-flag record's status"}), 200


@user.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    # registers a  new user
    user = User()
    data = request.get_json()
    check_fields_required(data)
    if len(errors) > 0:
        return jsonify(json.dumps(errors)), 400
    if user.check_if_user_exists(data['email'], data['password']):
        return jsonify({"message": "User already exists"}), 400
    user.insert_user(data)
    return jsonify({"message": "account has been successfully created",
                    "status": "200"}), 200


@user.route('/api/v2/auth/login', methods=['POST'])
def login():
    # this function enables user to log in
    data = request.get_json()
    login_fields = ['email', 'password']
    if not request.get_json:
        return jsonify({"msg": "JSON is missing in request"}, 'status', '400'), 400
    for field in login_fields:
        if field not in data.keys():
            return jsonify({"message": "Enter email and password"}), 400
    if new_user.check_if_user_exists(data['email'], data['password']):
        token = jwt.encode({'user': data['email'],
                            'exp': datetime.utcnow() +
                            timedelta(minutes=30)},
                           secret_key)
        return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({'message': 'Invalid email or password'}), 404



