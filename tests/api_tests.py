from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
import unittest
import requests
import base64
import dbfun
from models import *


TESTING = True



url = "http://127.0.0.1:8943"
import json
from app import app

class MyTest(TestCase):

    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ppadmin:admin@localhost/ppdb"
        self.db = SQLAlchemy(app)
        self.db.init_app(app)
        self.credentials = base64.b64encode(b"admin@admin.com:admin").decode("utf-8")
        return app

    def setUp(self):

        self.db.create_all()

    def tearDown(self):

        self.db.session.remove()
        self.db.drop_all()


    def test_01(self):
        with app.test_client() as c:
            testuser = {
                    "name":"testuser1",
                    "login":"testuser1@test.com",
                    "psw":"1"
                }
            response = c.post(url + "/users", data=json.dumps(testuser),headers={"Authorization": "Basic {}".format(self.credentials)},content_type='application/json')
        self.assert200(response)
        user = dbfun.get_model_by_login(User,testuser["login"])
        self.assertEqual(user.name,testuser["name"])
        self.assertEqual(user.login, testuser["login"])

    def test_02(self):
        with app.test_client() as c:
            testuser = {
                "name": "testuser2",
                "login": "testuser2@test.com",
                "psw": "2"
            }
            response = c.post(url + "/users", data=json.dumps(testuser),
                              headers={"Authorization": "Basic {}".format(self.credentials)},
                              content_type='application/json')
        self.assert200(response)
        user = dbfun.get_model_by_login(User, testuser["login"])
        self.assertEqual(user.name, testuser["name"])
        self.assertEqual(user.login, testuser["login"])

    def test_03(self):
        with app.test_client() as c:
            testuser = {
                "name": "testuser2"
            }
            response = c.post(url + "/users", data=json.dumps(testuser),
                              headers={"Authorization": "Basic {}".format(self.credentials)}
                              )
        self.assert400(response)

    def test_04(self):
        with app.test_client() as c:
            response = c.get(url + "/users/1",
                              headers={"Authorization": "Basic {}".format(self.credentials)},
                              content_type='application/json')
        self.assert200(response)

    def test_05(self):
        with app.test_client() as c:
            response = c.get(url + "/users/2",
                              headers={"Authorization": "Basic {}".format(self.credentials)},
                              content_type='application/json')
        self.assert403(response)


    def test_06(self):
        with app.test_client() as c:
            testuser = {
                "name": "admin",
                "login": "admin@admin.com",
                "psw": "admin"
            }
            response = c.put(url + "/users/1", data = json.dumps(testuser),
                              headers={"Authorization": "Basic {}".format(self.credentials)},
                              content_type='application/json')
        self.assert200(response)

    def test_07(self):
        with app.test_client() as c:
            testuser = {

            }
            response = c.put(url + "/users/1", data = json.dumps(testuser),
                              headers={"Authorization": "Basic {}".format(self.credentials)})
        self.assert400(response)

    def test_08(self):
        with app.test_client() as c:
            testuser = {
                "name": "admin",
                "login": "admin@admin.com",
                "psw": "admin"
            }
            response = c.put(url + "/users/0", data = json.dumps(testuser),
                              headers={"Authorization": "Basic {}".format(self.credentials)},
                              content_type='application/json')
        self.assert403(response)


if __name__ == '__main__':
    unittest.main()