from wit import Wit
from flask import request
from app import mongo
from flask_restful import Resource, reqparse

access_token = 'QGZM5YTXMY7PFBVGPEXJDP2FJ6EYOHRP'

client = Wit(access_token)
resp = client.message('осмотр детский')
print(resp, type(resp))
print(resp['entities']['doctor'][0]['value'])
print(resp['entities']['intent'][0]['value'])
