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

    def create_incident(self):
        # Tests that the incident is created
        response = self.client.post('/api/v2/interventions', 
                                    content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_fetch_all_incidents(self):
        # Tests that the end point fetches all incidents
        response = self.client.get('/api/v2/interventions',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_incident(self):
        # Tests that the end point returns a single incident
        self.client.post('api/v2/interventions',
                         json=self.incidents)
        response = self.client.get('/api/v2/interventions/1',
                                   content_type='application/json')
        msg = json.loads(response.data)
        print(msg)
        self.assertEqual(response.status_code, 200)

    def test_edit_incident(self):
        # Tests that the end point enables user edit their already
        #  created incident before status is changed by admin
        new_details = {
                    "title": "Corruption at its tipsefdthryt",
                    "description": "corruption in court in broad day light",
                    "status": "accepted",
                    "location": "mukono",
                    "record_type": "intervention",
                    "images": "fffff,fghjkj",
                    "videos": "ffcccdsffcvvbfff",
                    "created_by": "mutebiedfvfdhrtjuk",
                    "comments": "cuilrf,mrfre",
                    }
        response = self.client.patch('api/v2/interventions/1',json=new_details)
        print(response)
        msg = json.loads(response.data)
        self.assertIn("successfully edited", msg['data'])
        self.assertEqual(response.status_code, 200)

    def test_delete_incident(self):
        # Tests that the end point enables user edit their already created 
        # incident when rejected by admin
        incident_details = {
            "comments": "mutebiedfvfdhrtjuk",
            "created_by": "corruption in court in broad day light",
            "created_on": "Corruption at its tips  in kanjo",
            "description": "fffff,fghjkj",
            "images": "love",
            "location": "kakts",
            "record_id": 1,
            "record_type": "accepted",
            "status": "intervention",
            "title": "cuilrf,mrfre",
            "videos": "ffcccdsffcvvbfff"
            }
        self.client.post('api/v2/interventions',
                         content_type='application/json',
                         json=incident_details)
        response = self.client.delete('api/v2/interventions/1',
                                      content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn(" incident successfully deleted", msg['message'])
        self.assertEqual(response.status_code, 200)

    def tear_down(self):
        db = DatabaseConnection()
        db.drop_tables('records')
