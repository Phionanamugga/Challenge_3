from flask import jsonify, request, abort, Blueprint
from .models import Incident, User
from datetime import datetime
from api.models import Incident
import json
from database import DatabaseConnection
from api.validate import check_fields_required, errors
import jwt


incident = Blueprint('record', __name__)
user = Blueprint('user', __name__)

incident = Blueprint('record', __name__)
new_icident = Incident()                   
# new_user = User()


@incident.route('/api/v2/interventions', methods=['POST'])
def create_incident():
    data = request.get_json()
    created_incident = new_incident.add_incident(data)
    return jsonify({"message": " Successfully created",
                    "intervention": created_incident, "status" : 201}), 201


@incident.route('/api/v2/interventions', methods=['GET'])
def fetch_incident():
    # fetches all user's incidents
    fetched_incidents = new_incidents.get_incidents()
    return jsonify({'incidents': fetched_incidents, 'status':'200'}), 200


@incident.route('/api/v2/interventions/<int:incident_id>', methods=['GET'])
def fetch_single_incident(incident_id):
    fetched_incident = []
    fetched_incident = new_incident.fetch_single_incident(incident_id)
    if fetched_incident:
        return jsonify({"incident": fetched_incident, "status": "200"}), 200
    return jsonify({"message":"incident doesnot exist", "status": "404"}), 404


@incident.route('/api/v2/interventions/<int:incident_id>', methods=['PATCH'])
def edit_incident(incident_id):
    # This method updates a incident
    data = request.get_json()
    new_incident.update_incident(data['incident_type'],
                                 data['title'], data['description'], 
                                 data['location'], data['status'], 
                                 data['images'], data['videos'], data['comments'], incident_id)
    return jsonify({"status": 200,
                    "data": "successfully edited"}), 200


@incident.route('/api/v2/interventions/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    # this function enables user delete incident
    if incident_id == 0:
        return jsonify({"message": "This record doesnot exist", 'status': '400'}), 400
    new_icident.delete_incident(incident_id)
    return jsonify({"message": "incident successfully deleted"}), 200


@user.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    # registers a  new user
    data = request.get_json()
 

    # get the posted data
    # first_name = data['first_name']

    check_fields_required(data)
    if len(errors) > 0:
        return jsonify(json.dumps(errors)), 400    
    return jsonify({"message": "account has been successfully created", "status": "200"}), 200

    user = User()
    user.firstname = data['firstname']
    user.lastname = data['lastname']
    user.othername = data['othernames']
    user.password = hash_password(data['password'])
    user.email = data['email']
    user.phonenumber = data['phonenumber']
    user. username = data['username']

    user.insert_user()
    print(data)

    # key = 'edgsli,knw34r8743q23Q8WKDHYAW432'
    # password = '7rekcbjmezs'
    # new_pass = key + password
    # new_pass.encode('ascii')
    # encrypted_password = hashlib.sha256(new_pass).hexidigest()
    # print(encrypted_password)

    



    # validate the data
    # validate first_name
    # user_valid_data['first_name']
    # create the object. 
    # user = User()
    # user.firstname = first_name

    # user.insert_user()






@user.route('/api/v2/auth/login', methods=['POST'])
def login():
    # this function enables user to log in  
    data = request.get_json()
    login_fields = ['email', 'password']
    print(login_fields)
    # for field in login_fields:
    #     if field not in data.keys():
    #         return jsonify({"message": "Enter email and password"}), 400
    # if len(data.keys())> 2:
    #     return jsonify({"message": "Only email and password required"}), 400
    # if new_user.check_if_user_exists(data['email']) and new_user.check_password_match(data['password']):
        # access_token = create_access_token(identity=username)
        # return jsonify(access_token=access_token), 200
    # return jsonify({"message": "user doesnot exist, please register"}), 404