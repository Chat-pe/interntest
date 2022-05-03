from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_pymongo import PyMongo as pymongo
from flask_jwt_extended import JWTManager


import os

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])

CORS(app,  supports_credentials=True)
api = Api(app)
jwt = JWTManager(app)










from api import routes