from flask import Flask 
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

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(username):
    db.users.find_one({'username' : username})

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth/')

  return app