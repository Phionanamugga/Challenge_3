from flask import jsonify, request, abort, Blueprint
import re
import api.views


errors = {}
text_fields = ['othernames', 'firstname', 'lastname', 'username']
key_fields = ['email', 'password']
name_regex = r"[a-zA-Z]"
password_regex = r"(?=.*[0-9])"
username_regex = r"[a-zA-Z0-9_]"
phone_regex = r"\d{3}-\d{3}-\d{4}"


def check_fields_required(data={}):
    # check if required user field has data
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


def validate_logged_in_user(self, data):
    if not request.get_json:
        return jsonify({"msg": "JSON is missing in request"}, 'status', '400'), 400
    for field in login_fields:
        if field not in data.keys():
            return jsonify({"message": "Enter email and password"}), 400
    if new_user.check_if_user_exists(data['email']):
        token = jwt.encode({'user': data['username'],
                            'exp': datetime.utcnow() +
                            timedelta(hours=24)},
                           secret_key)
        return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({'message': 'user not found in list'}), 404


def create_incident():
    data = request.get_json()
    created_incident = new_incident.add_incident(data)
    return jsonify({"message": " Successfully created",
                    "intervention": created_incident, "status" : 201}), 201


def validate_fetch_single_incident(incident_id):
    fetched_incident = []
    fetched_incident = new_incident.fetch_single_incident(incident_id)


def fetch_incident():
    # fetches all user's incidents
    fetched_incidents = new_incidents.get_incidents()
    return jsonify({'incidents': fetched_incidents, 'status':'200'}), 200


def check_fetch_single_incident():
    # tests that a single user is fetched
    if fetched_incident:
        return jsonify({"incident": fetched_incident, "status": "200"}), 200
    return jsonify({"message": "incident doesnot exist", "status": "404"}), 404


def validate_edit_incident(incident_id):
    # This method updates a incident
    data = request.get_json()
    new_incident.update_incident(data['incident_type'],
                                 data['title'], data['description'], 
                                 data['location'], data['status'], 
                                 data['images'], data['videos'], data['comments'], incident_id)
    return jsonify({"status": 200,
                    "data": "successfully edited"}), 200


def validate_delete_incident(incident_id):
    # this function enables user delete incident
    if incident_id == 0:
        return jsonify({"message": "This record doesnot exist", 'status': '400'}), 400
    new_icident.delete_incident(incident_id)
    return jsonify({"message": "incident successfully deleted"}), 200