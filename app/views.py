import json
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
        FIO = data['FIO']
        photo = data['photo']

        g = open(f'{FIO}_face.jpg', 'wb')
        g.write(base64.b64decode(photo))
        files = {'file': (f'{FIO}.jpg', open(f'{FIO}_face.jpg', 'rb'), 'image/jpeg')}
        r = requests.post(PHOTO_REC_SERVER, files=files)

        response = json.loads(r.text)
        status = response['status']

        if status == 'success':
            id = response['id']
            data.pop('photo')
            data['id'] = id
            data['token'] = secrets.token_hex(16)
            mongo.db.users.insert_one(data)
            return {'status': 'OK', 'token': data['token']}
        else:
            return {'status': 'not OK'}


class LoginView(Resource):
    def post(self):
        data = request.json
        photo = data['photo']

        g = open(f'login_face.jpg', 'wb')
        g.write(base64.b64decode(photo))
        files = {'file': (f'login_face.jpg', open(f'login_face.jpg', 'rb'), 'image/jpeg')}
        r = requests.post(PHOTO_REC_SERVER + 'detect', files=files)
        result = open("result.html", "w")
        result.write(r.text)
        result.close()
        detected_person = json.loads(r.text)['detected person']
        print(detected_person)
        if detected_person != 'Unknown':
            return {'status': 'OK', 'detected_person': detected_person}
        else:
            return {'status': 'Not OK', 'detected_person': detected_person}
