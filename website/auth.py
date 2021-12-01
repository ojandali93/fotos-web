from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    data = request.form
    print(data)
  return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

  if request.method == 'POST':

    data = request.form
    username = data.get('username')
    password = data.get('password')
    print(password)
    password_confirm = data.get('password-confirm')
    print(password_confirm)
    name = data.get('name')
    account = data.get('account')
    location = data.get('location')
    bio = data.get('bio') 

    if len(username) < 6 or len(username) > 14:
      flash('username must be between 6 & 14 charactors.', category='error')
    elif len(password) < 6 or len(password) > 14:
      flash('passwird must be between 6 & 14 charactors.', category='error')
    elif password != password_confirm:
      flash('passwords do not match.', category='error')
    elif len(name) < 4:
      flash('name must be greater than 4 charactors.', category='error')
    else: 
      new_user = {
        'username': username,
        'password': password,
        'name': name,
        'account': account,
        'location': location,
        'bio': bio,
        'photo_list': [],
        'photo_count': 0,
        'edit_list':[],
        'edit_count': 0,
        'created_at': datetime.now()
      }

      db.users.insert_one(new_user)
      print(new_user)
      loggedInUser = new_user['username']
      flash('Account has been created.', category='success')

      return redirect(url_for('views.home', loggedInUser=loggedInUser))

  return render_template('signup.html')

@auth.route('/logout')
def logout():
  return "<h1> logout </h1>"

@auth.route('/admin')
def admin_home():
  all_users = db.users.find()
  return render_template('admin.html', all_users=all_users)