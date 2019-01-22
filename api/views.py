from flask import jsonify, request, abort, Blueprint
from .models import Record, User
from datetime import datetime
from api.models import Record
import json
import re
from database import DatabaseConnection

record = Blueprint('record', __name__)
user = Blueprint('user', __name__)

name_regex = r"[a-zA-Z]"
password_regex = r"(?=.*[0-9])"
username_regex = r"[a-zA-Z0-9_]"
phone_regex = r"\d{3}-\d{3}-\d{4}"
record = Blueprint('record', __name__)
new_record = Record()
new_user = User()


@record.route('/api/v2/interventions', methods=['POST'])
def create_record():
    data = request.get_json()
    created_record =  new_record.add_record(data)
    return jsonify({"message": " Successfully created", "intervention": created_record, "status" : 201}), 201


@record.route('/api/v2/interventions', methods=['GET'])
def fetch_record():
    # fetches all user's records
    fetched_records = new_record.get_record()
    return jsonify({'records': fetched_records})


@record.route('/api/v2/interventions/<int:record_id>', methods=['GET'])
def fetch_single_record(record_id):
    fetched_record = []
    fetched_record = new_record.fetch_single_record(record_id)
    if fetched_record:
        return jsonify({"record": fetched_record}), 200
    return jsonify({"message":"record doesnot exist"}), 404


@record.route('/api/v2/interventions/<int:record_id>', methods=['PUT'])
def edit_record(record_id):
    # This method updates a record
    data = request.get_json()
    new_record.update_record(data['record_type'],
                             data['title'], data['description'], 
                             data['location'], data['status'], 
                             data['images'], data['videos'],record_id, data['comments'])
    return jsonify({"status": 200,
                     "data": "successfully edited"}), 200


@record.route('/api/v2/interventions/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    # this function enables user delete record
    if record_id == 0 :
        return jsonify({"message": "This record doesnot exist"}), 400
    new_record.delete_record(record_id)
    return jsonify({"message": "record successfully deleted"}), 200


@user.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    # registers a  new user
    data = request.get_json()
    new_user = User()
    if new_user.check_if_user_exists(data['email']):
        return jsonify({"message": "This email already exists"})
    username = data['username']
    text_fields = ['othernames', 'firstname', 'lastname', 'username']
    user_fields = ['othernames', 'firstname', 'lastname']
    key_fields = ['email', 'password', 'isAdmin']
    for name in user_fields:
        if not re.match(name_regex, data[name]):
            return jsonify({'message': 'Enter correct ' + name + ' format'}), 400
    for text_field in text_fields:
        if len(data[text_field]) > 10:
            return jsonify({'message': text_field + ' too long'}), 404     
    for key in key_fields:
        if not data[key] or data[key].isspace():
            return jsonify({'message': key + ' field can not be empty.'}), 400   
        if not username or username.isspace():
            return jsonify({'message': 'Username can not be empty.'}), 400 
        if not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", data['email']):
            return jsonify({'message': 'Enter a valid email address.'}), 400
        if not re.match(username_regex, data['username']):
            return jsonify({'message': 'Enter a valid username'}), 400
        if not re.match(phone_regex, data['phonenumber']):
            return jsonify({'message': 'Enter phone format 123-456-7890'}), 400
        if len(data['password']) < 8:
            return jsonify({'message': 'Password must be atleast 8 characters'}), 400  
        new_user.insert_user(data)
        return jsonify({"message": " account has been successfully created"}), 201


@user.route('/api/v2/users', methods=['GET'])
def fetch_users():
# fetches all user's records
    all_users = new_user.fetch_users()
    return jsonify({'users': all_users})


@user.route('/api/v2/users/<int:user_id>', methods=['GET'])
# this fetches a single user account
def fetch_single_user_details(user_id):
    single_user = new_user.fetch_one_user(user_id)
    if single_user:
        return jsonify({"message": single_user}), 200
    return jsonify({"message": "User not found"}), 404


@user.route('/api/v2/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
# this function enables user to delete his/her account
    if user_id == 0:
        return jsonify({"message": "User doesnot exist"}), 400
    new_user.delete_user(user_id)
    return jsonify({"message": "account successfully deleted"}), 200


# @user.route('/api/v2/auth/login', methods=['POST'])
# def login():
# # this function enables user to log in  
#     data = request.get_json()
#     if not request.get_json:
#         return jsonify({"msg": "JSON is missing in request"}), 400
#         login_details = data.get('email', 'password')
#         password = data.get('password')
#     email = data.get('email')
#     for user in users:
#         if user.email == email:
#             return jsonify({'message': user.get_user_details()}), 200
#         if user.password == password:
#             return jsonify({'message': user.get_user_details()}), 200
#     return jsonify({'message': 'user not found in list'}), 404