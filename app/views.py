import json
import time
import base64
import secrets
import requests
from flask import request
from app import mongo
from flask_restful import Resource, reqparse


PHOTO_REC_SERVER = 'http://95.216.40.229:5000/'
parser = reqparse.RequestParser()


class TestView(Resource):
    def get(self):
        return {'hello': 'world'}


class RegisterView(Resource):
    def post(self):
        data = request.json
        photo = data['photo']
        token = secrets.token_hex(16)

        g = open(f'{token}.jpg', 'wb')
        g.write(base64.b64decode(photo))
        files = {'file': (f'{token}.jpg', open(f'{token}.jpg', 'rb'), 'image/jpeg')}
        r = requests.post(PHOTO_REC_SERVER, files=files)

        response = json.loads(r.text)
        status = response['status']

        if status == 'success':
            id = response['id']
            data.pop('photo')
            data['id'] = id
            data['token'] = token
            mongo.db.users.insert_one(data)
            response = {'request': 'register', 'status': 'OK', 'token': data['token']}
        else:
            response = {'request': 'register', 'status': 'not OK', 'error': response['error']}

        return response


class CorrectLoginView(Resource):
    def post(self):
        data = request.json
        photo = data['photo']

        g = open(f'login_face.jpg', 'wb')
        g.write(base64.b64decode(photo))
        g.close()
        files = {'file': (f'login_face.jpg', open(f'login_face.jpg', 'rb'), 'image/jpeg')}

        for i in range(100):
            try:
                r = requests.post(f'{PHOTO_REC_SERVER}detect', files=files)
                result = open("result.html", "w")
                result.write(r.text)
                result.close()
                break
            except requests.exceptions.ConnectionError:
                time.sleep(3)
        detected_person = json.loads(r.text)['detected person']

        if detected_person != 'Unknown':
            response = {'request': 'login', 'status': 'OK', 'detected_person': detected_person}
        else:
            response = {'request': 'login', 'status': 'Not OK', 'detected_person': detected_person}
        print(response)
        return response
