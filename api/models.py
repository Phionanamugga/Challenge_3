from database import DatabaseConnection
from datetime import datetime
from flask import jsonify


db = DatabaseConnection().cur


class Incident:
    # this class defines the record created by a user

    def __init__(self):
        self.incident_id = 0
        self.createdon = ""
        self.record_type = ""
        self.title = ""
        self.description = ""
        self.location = ""
        self.status = ""
        self.images = ""
        self.videos = ""
        self.comments = ""

    def add_incident(self, data):
        createdon = datetime.utcnow()
        # SQL query to add a record to the database
        query = """
        INSERT INTO incidents(createdon, created_by, incident_type, title,
        description, location, status, images, videos,comments)\
        self

        VALUES('{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}') RETURNING *; 
        """.format(createdon, data['created_by'], data['incident_type'],
                   data['title'], data['description'], data['location'],
                   data['status'], data['images'], data['videos'], data['comments'])
        db.execute(query)
        created_incident = db.fetchone()
        return created_incident       

    def get_incident(self):
        # Fetches all records from the database
        incidents = []
        sql = """SELECT * FROM records"""
        db.execute(sql)
        rows = db.fetchall()
        for row in rows:
            incidents.append({
                "incident_id": row[0],
                "created_on": row[1],
                "created_by": row[2],
                "record_type": row[3],
                "title": row[4],
                "description": row[5],
                "location": row[6],
                "status": row[7],
                "images": row[8],
                "videos": row[9],
                "comments": row[10]
            })

        return incidents

    def delete_incident(self, incident_id):
        # This function deletes an incident from the database
        query = """DELETE * FROM incidents WHERE incident_id = '{}';"""
        db.execute.format(query)

    def fetch_single_incident(self, incident_id):
        # Fetches a single an incident from the database
        single_incident = []
        sql = """ SELECT * FROM incidents WHERE incident_id = {}"""
        db.execute.format(sql)
        row = db.fetchone()
        if row:
            single_incident.append({
                "incident_id": row[0],
                "createdon": row[1],
                "created_by": row[2],
                "record_type": row[3],
                "title": row[4],
                "description": row[5],
                "location": row[6],
                "status": row[7],
                "images": row[8],
                "videos": row[9],
                "comments": row[10]
            })
            return single_incident
            
    def update_incident(self, incident_type, title,
                        description, location, status, 
                        images, videos, comments, incident_id):
        # Modifies a record
        sql = f"""UPDATE incidents SET incident_type='{incident_type}',\
                 title='{title}', description ='{description}', location='{location}',\
                 status='{status}', images='{images}', videos='{videos}',
                 comments='{comments}' WHERE incident_id='{incident_id}';"""
        db.execute(sql)


class User:
    # this class defines the details of a user
    def __init__(self):
        self.user_id = 0
        self.firstname = ""
        self.lastname = ""
        self. othernames = ""
        self. email = ""
        self.password = ""
        self.phonenumber = ""
        self.username = ""
        self. registered_on = ""
        dbconn = DatabaseConnection()
        dbconn.create_user_table()

    def insert_user(self, data):
        registered_on = datetime.utcnow()
        """SQL query to add a new user to the database"""
        query = """
        INSERT INTO users(firstname, lastname, othernames, email,
                          password, phonenumber, username, registered_on)\
        VALUES('{}', '{}', '{}', '{}', '{}','{}','{}','{}');
        """.format(data['firstname'], data['lastname'], 
           data['othernames'], data['email'], data['password'],
           data['phonenumber'], data['username'], registered_on)

        db.execute.format(query)
    
    def check_if_user_exists(self, email):
        sql = """  SELECT * FROM users WHERE email = '{}';"""
        db.execute(sql.format(email))
        row = db.fetchone()
        if row:
            return True
        return False
    
    def fetch_users(self):
        # Fetches all users from the database
        user_rows = []
        sql = """SELECT * FROM users;"""
        db.execute(sql)
        rows = db.fetchall()
        for row in rows:
            user_rows.append({
                "user_id": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "othernames": row[3],
                "email": row[4],
                "password": row[5],
                "phonenumber": row[6],
                "username": row[7],
                "registered_on": row[8]
                
            })
        return user_rows

    def fetch_one_user(self, user_id):
        # returns a single user from the database
        sql = """SELECT * FROM users WHERE user_id = '{}';"""
        db.execute.format(sql)
        user_row = db.fetchone()
        if user_row:
            return {
                "user_id": user_row[0],
                "firstname": user_row[1],
                "lastname": user_row[2],
                "othernames": user_row[3],
                "email": user_row[4],
                "password": user_row[5],
                "phonenumber": user_row[6],
                "username": user_row[7],
                "registered_on": user_row[8] 
              }

    def delete_user(self, user_id):
        # Deletes a user from the database
        sql = """DELETE FROM users WHERE user_id='{}';"""
        db.execute.format(sql)

    def check_password_match(self, password):
        # checks if supplied password matches stored password
        sql = """SELECT * FROM users WHERE password = '{}';"""
        db.execute.format(sql)
        fetched_password = db.fetchall()
        if fetched_password:
            return True
        return False