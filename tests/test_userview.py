import unittest
import json
from api import app
from database import DatabaseConnection


class Test_user_views(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db = DatabaseConnection()
        db.create_user_table()

    def test_register_user(self):
        # Tests that the end point enables a new user create an account
        
        user_details = {
                        "firstname": "emily",
                        "lastname": "mirembe",
                        "othernames": "princess",
                        "password": "12345678",
                        "email": "email@gmail.com",
                        "phonenumber": "0756723881",
                        "username": "phiona", 
                        "is_admin": "False"         
                        }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json', 
                                    data=json.dumps(user_details))
        print(response.data)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("account has been successfully created", msg['message'])

    def test_user_login(self):
        # Tests that the end point enables a user_login
        login_details = {"email": "email@gmail.com",
                         "password": "12345678"}
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(login_details))
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def tear_down(self):
        db = DatabaseConnection()
        db.drop_tables('users')