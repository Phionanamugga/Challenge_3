import unittest
import json
from api import app
from database import DatabaseConnection

db = DatabaseConnection() 


class Test_user_views(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()    
        db.create_user_table() 
        self.user_details = {
                        "firstname": "emily",
                        "lastname": "mirembe",
                        "othernames": "princess",
                        "password": "123456Aa78",
                        "email": "phiona@gmail.com",
                        "phonenumber": "0756723881",
                        "username": "phiona", 
                        "is_admin": "False"         
                        }
        self.login_details = {
                    "email": "phiona@gmail.com",
                    "password": "123456Aa78"
                    }
    
    def test_register_user(self):
        # Tests that the end point enables a new user create an account
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json', 
                                    data=json.dumps(self.user_details))
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("account has been successfully created", msg['message'])

    def test_user_login(self):
        # Tests that the end point enables a user_login
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=self.login_details)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_with_wrong_key_fileds(self):
        # Tests that the end point doesnot login with invalid data
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        wrong_credentials = {
            "username": "phiona",
            "password": "1234phio"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=wrong_credentials)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_user_login_without_data(self):
        # Tests that the end point doesnot login with invalid data
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        wrong_credentials = {
            
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=wrong_credentials)
        msg = json.loads(response.data)
        self.assertIn("Enter email and password",msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_invalid_data(self):
        # Tests that the end point doesnot login with invalid data
        self.client.post('/api/v2/auth/signup',
                         content_type='application/json', 
                         data=json.dumps(self.user_details))
        wrong_credentials = {
            "email": "phiona@mail.com",
            "password": "1234phio"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=wrong_credentials)
        msg = json.loads(response.data)
        self.assertIn("Invalid email or password",msg['message'])
        self.assertEqual(response.status_code, 404)

    def tearDown(self):    
        db.drop_tables('users')