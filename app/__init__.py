from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/database'
mongo = PyMongo(app)

from app.views import *

api = Api(app)
api.add_resource(TestView, '/test')
api.add_resource(LoginView, '/login')
api.add_resource(RegisterView, '/register')
