from flask import Flask, session, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
from os import path
from flask_login import LoginManager

client = MongoClient()
db = client.Contractor 

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'eigeinsonriuosvnirosjvsoe' 

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth/')

  return app