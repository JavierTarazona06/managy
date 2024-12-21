import json
from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Amenity
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#import requests

import base64
import requests


class AdminTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        cls.username = 'admin@admin.com'
        cls.mypassword = 'zdLFekMpNj08'

        create_data = {
            'name': "nameRecr",
            'address': "addressRecr",
            'photo': "https://storage.googleapis.com/managy_bucket/images//El%20Country_w6w1V.png"
        }

        response = client.post(
            '/api/recreational_venue/create/', create_data
        )

        create_data = {
            "first_name": "name",
            "email": cls.username,
            "password": cls.mypassword,
            "recreational_venue_id": response.data['id'],
            "dob": date(1990, 5, 10),
            "telephone": "1234567890",
            "address": "address"
        }

        client.post(
            '/users/register/admin/', create_data
        )

        response = client.post(
            '/api/token/', {'username': cls.username, 'password': cls.mypassword}
        )
        assert response.status_code == 200  # Ensure token generation works during setup

        cls.token = response.json()['access']
        credentials = f"{cls.username}:{cls.mypassword}"
        cls.basic_token = base64.b64encode(credentials.encode()).decode()
        cls.header_basic = {
            'Authorization': f'Basic {cls.basic_token}',
            'Content-Type': 'application/json'
        }
        cls.header = {"Authorization": f"Bearer {cls.token}"}

    def setUp(self):
        pass


    def test_log_in_m(self):
        """
        login
        """
        print("TEST:login_m")
        response = self.client.post(
            '/api/token/',
            {
                "username": "one@one.com",
                "password": "Hola1234$"
            }
        )
        self.assertEqual(response.json()['detail'], "No active account found with the given credentials")
        self.assertEqual(response.status_code, 401)


    def test_C_recr_ven(self):
        print("test_C_recr_ven")
        create_data = {
            "name": "Club 1",
            "address": "arrra  57",
            "photo": "https://storage.googleapis.com/managy_bucket/images//El%20Country_w6w1V.png"
        }
        response = self.client.post(
            '/api/recreational_venue/create/',
            data = create_data
        )
        dict_result = {
            "id": 2,
            "name": "Club 1",
            "address": "arrra  57",
            "photo": "https://storage.googleapis.com/managy_bucket/images//El%20Country_w6w1V.png"
        }
        self.assertEqual(response.json(), dict_result)
        self.assertEqual(response.status_code, 201)

    def test_C_admin(self):
        print("test_C_admin")
        data_in = {
            "first_name": "admin1",
            "email": "admin1@admin1.com",
            "password": "admin1",
            "recreational_venue_id": 1,
            "dob": "2024-10-28",
            "telephone": "52851",
            "address": "sss"
        }
        response = self.client.post(
            '/users/register/admin/',
            data_in
        )

        dict_result = {
            "id": 2,
            "first_name": "admin1",
            "email": "admin1@admin1.com",
            "role": "admin",
            "username": "admin1@admin1.com",
            "recreational_venue": [
                1
            ],
            "dob": "2024-10-28",
            "telephone": "52851",
            "address": "sss"
        }
        self.assertEqual(response.json(), dict_result)
        self.assertEqual(response.status_code, 201)


    def test_C_worker(self):
        print("test_C_worker")
        data_in = {
            'first_name': "worker",
            'email': "worker@worker.com",
            'role': "worker",
            'recreational_venue_id': None
        }
        response = self.client.post(
            '/users/admin/createuser/',
            data=json.dumps(data_in), headers=self.header,
            content_type='application/json'
        )

        dict_result = {
            "id": 4,
            "first_name": "worker",
            "email": "worker@worker.com",
            "role": "worker"
        }
        self.assertEqual(response.json(), dict_result)
        self.assertEqual(response.status_code, 201)


    def test_C_member(self):
        print("test_C_member")
        data_in = {
            "first_name": "member",
            "email": "member@member.com",
            "role": "member",
            "recreational_venue_id": None
        }
        response = self.client.post(
            '/users/admin/createuser/',
            data=data_in, headers=self.header,
            content_type='application/json'
        )

        dict_result = {
            "id": 3,
            "first_name": "member",
            "email": "member@member.com",
            "role": "member"
        }
        self.assertEqual(response.json(), dict_result)
        self.assertEqual(response.status_code, 201)


    def test_D_usr(self):
        print("test_D_usr")
        data_in = {
            "first_name": "member1",
            "email": "member1@member1.com",
            "role": "member",
            "recreational_venue_id": None
        }
        response = self.client.post(
            '/users/admin/createuser/',
            data_in, headers=self.header,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(
            f'/users/admin/deleteuser/{response.json()["id"]}/',
            headers=self.header, content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)


    def test_C_usr_batch(self):
        print("test_C_usr_batch")
        '''
        data_in = {
            "role": "member",
            "excel_link": "https://storage.googleapis.com/download/storage/v1/b/managy_bucket/o/admin_excel%2Ftestbatchcreation.xlsx?generation=1730534493063868&alt=media"
        }
        response = self.client.post(
            '/user/admin/createuserbatch/',
            data_in, headers=self.header
        )
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        dict_result = {
            "message": "Users Successfully Created"
        }
        self.assertEqual(response.json(), dict_result)
        '''
        data_in = {
            "email": "one@one.com"
        }
        response = self.client.post(
            '/user/resetpassword/',
            data_in
        )
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 404)
        dict_result = {'error': 'User with credentials not found'}
        self.assertEqual(response.json(), dict_result)

        response = self.client.get(
            '/api/admin/search/',
            headers=self.header, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        dict_result = [{'id': 1, 'first_name': 'name', 'email': 'admin@admin.com', 'role': 'admin', 'username': 'admin@admin.com', 'recreational_venue': [1]}]
        '''
        dict_result = [
            {
                "id": 1,
                "first_name": "admin",
                "email": "admin@admin.com",
                "role": "admin",
                "username": "admin@admin.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 2,
                "first_name": "worker",
                "email": "worker@worker.com",
                "role": "worker",
                "username": "worker@worker.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 4,
                "first_name": "one",
                "email": "one@one.com",
                "role": "member",
                "username": "one@one.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 5,
                "first_name": "two",
                "email": "two@one.com",
                "role": "member",
                "username": "two@one.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 6,
                "first_name": "three",
                "email": "three@one.com",
                "role": "member",
                "username": "three@one.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 7,
                "first_name": "four",
                "email": "four@one.com",
                "role": "member",
                "username": "four@one.com",
                "recreational_venue": [
                    1
                ]
            },
            {
                "id": 8,
                "first_name": "five",
                "email": "five@one.com",
                "role": "member",
                "username": "five@one.com",
                "recreational_venue": [
                    1
                ]
            }
        ]
        '''
        print(response.json())
        self.assertEqual(response.json(), dict_result)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

class MemberTest():
    #One for CRUD users
    #One for CRUD events/amenities
    pass

class WorkerTest():
    pass