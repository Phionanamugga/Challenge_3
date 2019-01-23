from flask import jsonify, request, abort, Blueprint
import re
errors = {}
text_fields = ['othername', 'firstname', 'lastname', 'username']
key_fields = ['email', 'password']
name_regex = r"[a-zA-Z]"
password_regex = r"(?=.*[0-9])"
username_regex = r"[a-zA-Z0-9_]"
phone_regex = r"\d{3}-\d{3}-\d{4}"


def check_fields_required(data={}):
    # check if require field has data
    for name in text_fields:
        if not re.match(name_regex, data[name]):
            return jsonify({'message': 'Enter correct ' + name + ' format', 'status': '400'}), 400 
    
    for text_field in text_fields:
        if len(data[text_field]) > 10:
            return jsonify({'message': text_field + ' too long','status': '404'}), 404

    for key, value in data.items():
        if key != 'othername' and not value:
            errors[key] = f'{key} is required'
            return jsonify({'message': key + ' field can not be empty.', 'status': '400'}), 400  

        if not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", data['email']):
            return jsonify({'message': 'Enter a valid email address.','status': '400'}), 400

        if not re.match(phone_regex, data['phonenumber']):
            return jsonify({'message': 'Enter phone format 123-456-7890', 'status':'400'}), 400

        if len(data['password']) < 8:
            return jsonify({'message': 'Password must be atleast 8 characters','status':'400'}), 400  
    return jsonify({"message": " account has been successfully created",'status': '201'}), 201
  

def check_userlogin_requirements(email, password):
    # tests that the required login details are filled in before the user logs in 
    if not request.get_json:
        return jsonify({"msg": "JSON is missing in request"}, 'status', '400'), 400
    for field in login_fields:
        if field not in data.keys():
            return jsonify({"message": "Enter email and password"}), 400
    for user in users:
        if user.email == email and user.password == password:
            return jsonify({'message': "logged",'status': '201'}), 201
    return jsonify({'message': 'user not found in list'}), 404


def check_fetch_single_incident():
    # tests that a singlu user is fetched
    if fetched_incident:
        return jsonify({"incident": fetched_incident, "status": "200"}), 200
    return jsonify({"message": "incident doesnot exist", "status": "404"}), 404

