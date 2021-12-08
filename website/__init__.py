from flask import Flask, session, redirect, url_for
from pymongo import MongoClient
from os import path, mkdir

client = MongoClient()
db = client.Contractor 

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'eigeinsonriuosvnirosjvsoe' 
upload_folder = 'website/static/'
if not path.exists(upload_folder):
  mkdir(upload_folder)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = upload_folder

from .views import views
from .auth import auth
from .post import post
from .edit import edit

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth/')
app.register_blueprint(post, url_prefix='/post/')
app.register_blueprint(edit, url_prefix='/edit/')


def create_app():

  return app