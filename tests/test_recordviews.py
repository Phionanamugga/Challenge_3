import unittest
import json
from api import app
from database import DatabaseConnection


class Test_record_views(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fetch_all_records(self):
        # Tests that the end point fetches all records
        response = self.client.get('/api/v2/interventions',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_record(self):
        # Tests that the end point returns a single record
        records = {
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
        self.client.post('api/v2/interventions',
                         json=records)
        response = self.client.get('/api/v2/interventions/1',
                                   content_type='application/json')
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_edit_record(self):
        # Tests that the end point enables user edit their already
        # created record before status is changed by admin
        record_details = {
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
        response = self.client.post(
            'api/v2/interventions',
            content_type='application/json', 
            json=record_details
        )
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
        response = self.client.put('api/v2/interventions/1',json=new_details)
        print(response)
        msg = json.loads(response.data)
        self.assertIn("successfully edited", msg['message'])
        self.assertEqual(response.status_code, 200)

    def test_delete_record(self):
        # Tests that the end point enables user edit their already created
        # record when rejected by admin
        record_details = {
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
        response = self.client.post('api/v2/interventions',
                                    content_type='application/json',
                                    json=record_details)
        new_details = {
        }
        response = self.client.delete('api/v2/interventions/1',
                                      json=new_details)
        msg = json.loads(response.data)
        self.assertIn("successfully deleted", msg['message'])
        self.assertEqual(response.status_code, 200)

   