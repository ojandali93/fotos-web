from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from bson.objectid import ObjectId

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

  if 'username' in session:

    return redirect(url_for('views.home'))

  else:

    if request.method == 'POST':
      data = request.form
      username = data.get('username')
      password = data.get('password')
      checked_user = db.users.find_one({'username' : username})
      if checked_user:
        if check_password_hash(checked_user['password'], password):
          flash('Logged in successfully.', category='success')
          session["username"] = username
          return redirect(url_for('views.home'))
        else:
          flash('Incorrect password. Try again.', category='error')
      else:
        flash('Email does not exist in our records.', category='error')

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

  if 'username' in session:

    return redirect(url_for('views.hom'))

  else:

    if request.method == 'POST':

      data = request.form
      username = data.get('username')
      password = data.get('password')
      print(password)
      password_confirm = data.get('password-confirm')
      print(password_confirm)
      email = data.get('email')
      name = data.get('name')
      account = data.get('account')
      location = data.get('location')
      bio = data.get('bio') 

      check_username = db.users.find_one({'username' : username})
      check_email = db.users.find_one({'email' : email})

      if check_username:
        flash('username already exists', category='error')
      elif check_email: 
        flash('Email already exists.', category='error')
      elif len(username) < 6 or len(username) > 14:
        flash('username must be between 6 & 14 charactors.', category='error')
      elif len(password) < 6 or len(password) > 14:
        flash('passwird must be between 6 & 14 charactors.', category='error')
      elif password != password_confirm:
        flash('passwords do not match.', category='error')
      elif len(name) < 4:
        flash('name must be greater than 4 charactors.', category='error')
      else: 
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = {
          'username': username,
          'password': hashed_password,
          'email': email,
          'name': name,
          'account': account,
          'location': location,
          'bio': bio,
          'photo_list': [],
          'photo_count': 0,
          'downloads': [],
          'downloads_count': 0,
          'edit_list':[],
          'edit_count': 0,
          'followers': [],
          'follower_count': 0,
          'following': [],
          'follwering_count': 0,
          'created_at': datetime.now()
        }

        db.users.insert_one(new_user)
        current_user = db.users.find_one({'username' : username})
        flash('Account has been created.', category='success')
        session['username'] = username

        return redirect(url_for('views.home'))

  return render_template('signup.html')

@auth.route('/logout')
def logout():

  if 'username' in session:
    session.pop('username', None)

  return redirect(url_for('auth.login'))

@auth.route('/admin')
def admin_home():

  all_users = db.users.find()

  return render_template('admin.html', all_users=all_users)