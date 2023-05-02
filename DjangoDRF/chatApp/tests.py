import unittest
from django.test import Client
from .views import getchat, thread, openchats
from django.urls import reverse
import json

client= Client()

class ClassCreationTest(unittest.TestCase):
    classes = ""

    def setUp(self):
        self.getchaturl = reverse(getchat)
        self.threadurl = reverse(thread)
        self.openchatsurl = reverse(openchats)

    def test_getchat(self):
        '''
        This method is used to test the getchat method
        '''

        # test with valid data
        data = json.dumps({
            "user_id": 1,
            "user_type": "EMAIL",
            "friend_id": 2,
            "friend_type": "EMAIL"
        })

        response = client.post(self.getchaturl, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_openchats_invalid_id(self):
        '''
        This method is used to test the openchats method
        '''

        data = json.dumps({
            "user_id": 1,
            "user_type": "EMAIL",
            "friend_id": 100,
            "friend_type": "EMAIL"
        })

        response = client.post(self.getchaturl, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_thread(self):
        '''
        This method is used to test the thread post method
        '''

        # test with post method with valid data
        data = json.dumps({
            "user_id": 1,
            "user_type": "EMAIL",
            "friend_id": 2,
            "friend_type": "EMAIL"
        })

        response = client.post(self.threadurl, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_thread_invalid_id(self):
        '''
        This method is used to test the thread post method
        '''

        # test with post method with invalid data
        data = json.dumps({
            "user_id": 1,
            "user_type": "EMAIL",
            "friend_id": 100,
            "friend_type": "LINKEDIN"
        })

        response = client.post(self.threadurl, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_thread_get(self):
        '''
        This method is used to test the thread get method
        '''

        # test with get method with valid data
        
        query_params = {
            "id": 1
        }

        response = client.get(self.threadurl, data=query_params, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_thread_invalid_id(self):
        '''
        This method is used to test the thread get method
        '''

        # test with get method with valid data
        
        query_params = {
            "id": abc
        }

        response = client.get(self.threadurl, data=query_params, content_type='application/json')
        self.assertEqual(response.status_code, 404)



    

