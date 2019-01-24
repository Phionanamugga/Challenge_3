import unittest
import json
from api import app
from database import DatabaseConnection


class Test_record_views(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()      
        db = DatabaseConnection()
        db.create_incident_table()
        self.incidents = {
                    "title": "Corruption at its tipsefdthryt",
                    "description": "corruption in court in broad day light",
                    "status": "Resolved",
                    "location": "nansana",
                    "record_type": "redflag",
                    "images": "fffff,fghjkj",
                    "videos": "ffcccdsffcvvbfff",
                    "created_by": "mutebiedfvfdhrtjuk",
                    "comments": "cuilrf,mrfre"
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
        # Tests that the incident is created
        response = self.client.post('/api/v2/interventions', 
                                    content_type= 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_fetch_all_incidents(self):
        # Tests that the end point fetches all incidents
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        resp = self.client.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.login_details))
        msg = json.loads(resp.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.get('/api/v2/interventions',
                                   headers=headers
                                   )
        self.assertEqual(response.status_code, 200)

    # def test_fetch_single_incident(self):
    #     # Tests that the end point returns a single incident
    #     self.client.post('api/v2/interventions',
    #                      json=self.incidents)
    #     response = self.client.get('/api/v2/interventions/1',
    #                                content_type='application/json')
    #     msg = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_incident(self):
    #     # Tests that the end point enables user edit the location to their
    #     #  created incident before status is changed by admin
    #     new_location = {
                
    #                 "location": "mukono",
    #                 }
    #     response = self.client.patch('/api/v2/interventions/<int:incident_id>/location', json = new_location)
    #     print(response)
    #     msg = json.loads(response.data)
    #     self.assertIn("Updated the  intervention record's location", msg['data'])
    #     self.assertEqual(response.status_code, 200)


    # def test_edit_incident(self):
    #     # Tests that the end point enables user edit   comment to their
    #     #  created incident before status is changed by admin
    #     new_comment = {"comment": "I have added videos" }
    #     response = self.client.patch('/api/v2/red-flag/<int:incident_id>/comment', json = new_comment)
    #     print(response)
    #     msg = json.loads(response.data)
    #     self.assertIn("Updated the  intervention record's comment", msg['data'])
    #     self.assertEqual(response.status_code, 200)


    # def test_edit_incident(self):
    #     # Tests that the end point enables user edit   comment to their
    #     #  created incident before status is changed by admin
    #     new_location = {"comment": "Emergency intervention required" }
    #     response = self.client.patch('/api/v2/red_flag/<int:incident_id>/comment', json = new_comment)
    #     print(response)
    #     msg = json.loads(response.data)
    #     self.assertIn("Updated the  red-flag record's location", msg['data'])
    #     self.assertEqual(response.status_code, 200)


    # def test_edit_incident(self):
    #     # Tests that the end point enables user edit   comment to their
    #     #  created incident before status is changed by admin
    #     new_comment = {"comment": "Emergency intervention required" }
    #     response = self.client.patch('/api/v2/redflag/<int:incident_id>/comment', json = new_comment)
    #     print(response)
    #     msg = json.loads(response.data)
    #     self.assertIn("Updated the  red-flag record's location", msg['data'])
    #     self.assertEqual(response.status_code, 200)


    # def test_delete_incident(self):
    #     # Tests that the end point enables user edit their already created 
    #     # incident when rejected by admin
    #     incident_details = {
    #         "comments": "mutebiedfvfdhrtjuk",
    #         "created_by": "corruption in court in broad day light",
    #         "created_on": "Corruption at its tips  in kanjo",
    #         "description": "fffff,fghjkj",
    #         "images": "love",
    #         "location": "kakts",
    #         "record_id": 1,
    #         "record_type": "accepted",
    #         "status": "intervention",
    #         "title": "cuilrf,mrfre",
    #         "videos": "ffcccdsffcvvbfff"
    #         }
    #     self.client.post('api/v2/interventions',
    #                      content_type='application/json',
    #                      json=incident_details)
    #     response = self.client.delete('api/v2/interventions/1',
    #                                   content_type='application/json')
    #     msg = json.loads(response.data)
    #     self.assertIn(" incident successfully deleted", msg['message'])
    #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db = DatabaseConnection()
        db.drop_tables('incidents')
