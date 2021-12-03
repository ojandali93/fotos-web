from flask import Blueprint, render_template, session, redirect, url_for
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():

  if 'username' in session:
    username = session['username']
  else:
    return redirect(url_for('auth.login'))

  return render_template('home.html')
