import unittest
import json
from api import app
from database import DatabaseConnection
from api.views import token_required


class Test_record_views(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()      
        db = DatabaseConnection()
        db.create_incident_table()
        self.incidents = {
                "incident_type": "Articlkhje",
                "title": "Incident at Kamwokya",
                "description": "Today is the day",
                "location": "Kamwokya",
                "status": "unresolved",
                "images": "image",
                "videos": "video",
                "comments": "hello",
                "created_by": "phiona"
            }
         
        self.user_details = {
                        "firstname": "emily",
                        "lastname": "mirembe",
                        "othernames": "princess",
                        "password": "12345678",
                        "email": "email@gmail.com",
                        "phonenumber": "0756723881",
                        "username": "phiona", 
                        "is_admin": "False"         
                        }
        self.login_details = {"email": "email@gmail.com",
                              "password": "12345678"}

    def test_create_incident(self):
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.login_details))
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.get('/api/v2/interventions/1',
                                   headers=headers
                                   )
        self.assertEqual(response.status_code, 200)    

    def test_fetch_all_incidents(self):
        # Tests that the end point fetches all incidents
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.login_details))
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.get('/api/v2/interventions',
                                   headers=headers
                                   )
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_incidents(self):
        # Tests that the end point returns a single incident
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(self.login_details))
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.get('/api/v2/interventions/1',
                                   headers=headers
                                   )
        self.assertEqual(response.status_code, 200)

    def test_edit_incident(self):
        # Tests that the end point enables user edit   comment to their
        #  created incident before status is changed by admin
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))

        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))

        message = json.loads(resp.data)
        token = message['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
            }
        self.client.post('/api/v2/interventions',
                         headers=headers,
                         json=self.incidents)
        self.status = {
            "status": "I have added videos"
            }

        response = self.client.patch('/api/v2/interventions/1/status',
                                     headers=headers,
                                     json=self.status)
        msg = json.loads(response.data)
        self.assertIn("Updated red-flag record's status", msg['data'])
        self.assertEqual(response.status_code, 200)

    def test_edit_incident_location(self):
        # Tests that the end point enables user edit   comment to their
        #  created incident before status is changed by admin
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))

        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))

        message = json.loads(resp.data)
        token = message['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
            }
        self.client.post('/api/v2/interventions',
                         headers=headers,
                         json=self.incidents)
        new_location = {
            "location": "Emergency intervention required"
            }
        response = self.client.patch('/api/v2/interventions/1/location',
                                     headers=headers,
                                     json=new_location)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_edit_incident_comment(self):
        # Tests that the end point enables user edit   comment to their
        #  created incident before status is changed by admin
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))

        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))

        message = json.loads(resp.data)
        token = message['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
            }
        self.client.post('/api/v2/interventions',
                         headers=headers,
                         json=self.incidents)
        self.new_comment = {
            "comment": "Emergency intervention required"
             }
               
        response = self.client.patch('/api/v2/interventions/1/comment',
                                     headers=headers,
                                     json=self.new_comment)
        print(response)
        msg = json.loads(response.data)
        self.assertIn("Updated intervention record's comment", msg['data'])
        self.assertEqual(response.status_code, 201)

    def test_delete_incident(self):
        # Tests that the end point enables user can delete his or her already created 
        # incident when rejected by admin
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))

        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))

        message = json.loads(resp.data)
        token = message['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
            }
        self.client.post('/api/v2/interventions',
                         headers=headers,
                         json=self.incidents)

        response = self.client.delete('/api/v2/interventions/1',
                                      headers=headers,
                                      json=self.incidents)
        message = json.loads(response.data)
        self.assertIn("incident successfully deleted", message['message'])
        self.assertEqual(response.status_code, 200)

    def test_delete_incident_for_wrong_incident_id(self):
        # Tests that the end point enables user can delete his or her already created 
        # incident when rejected by admin
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))

        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))

        message = json.loads(resp.data)
        token = message['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
            }
        self.client.post('/api/v2/interventions',
                         headers=headers,
                         json=self.incidents)

        response = self.client.delete('/api/v2/interventions/0',
                                      headers=headers,
                                      json=self.incidents)
        message = json.loads(response.data)
        self.assertIn("This record doesnot exist", message['message'])
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        db = DatabaseConnection()
        db.drop_tables('users')
