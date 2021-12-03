from flask import Blueprint, render_template, session, redirect, url_for, request
from . import db

views = Blueprint('views', __name__)

@views.route('/profile', methods=(['GET']))
def profile():
  if 'username' in session:
    print('profile page')
    print(session['username'])
    loggedInUser = db.users.find_one({'username': session['username']})
    return render_template('profile.html', loggedInUser=loggedInUser)
  else:
    return redirect(url_for('auth.login'))

@views.route('/profile/edit', methods=['GET', 'POST'])
def profile_update():
  if 'username' in session:
    loggedInUser = db.users.find_one({'username': session['username']})
    print(loggedInUser)
    if request.method == 'POST':
      pass
    else:
      return render_template('update_profile.html', loggedInUser=loggedInUser)
  else:
    return redirect(url_for('auth.login'))

@views.route('/')
def home():

  if 'username' in session:
    username = session['username']
  else:
    return redirect(url_for('auth.login'))

  return render_template('home.html')
