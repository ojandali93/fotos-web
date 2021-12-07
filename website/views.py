from flask import Blueprint, render_template, session, redirect, url_for, request
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
  if 'username' in session:
    username = session['username']
    current_user = db.users.find_one({'username': session['username']})
    feed = []
    current_user_following = current_user['following']
    for follower in current_user_following:
      follower_photos = follower['photo_list']
      for photo in follower_photos:
        feed.append(photo)
      follower_edits = follower['edit_list']
      for photo in follower_edits:
        feed.append(photo)
    feed.sort(key=sortFeed)
    feed.sort(reverse=True)
    return render_template('home.html', feed=feed)
  else:
    return redirect(url_for('auth.login'))

@views.route('/profile', methods=(['GET']))
def profile():
  if 'username' in session:
    print('profile page')
    print(session['username'])
    loggedInUser = db.users.find_one({'username': session['username']})
    return render_template('profile.html', loggedInUser=loggedInUser)
  else:
    return redirect(url_for('auth.login'))

# TODO: Update the update_profile html file. 
  # not rendering correct information into the form fields
  # need to complete the form processing
  # check how to make sure the correct account type is displayed and selected
  # should redirect to home
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

@views.route('/photos', methods=['GET'])
def user_photos():
  if 'username' in session:
    all_photos = db.posts.find({'author': session['username'], 'is_original': True})
    return render_template('user_photos.html', all_photos=all_photos)
  else:
    return redirect(url_for('auth.login'))

@views.route('/edits', methods=['GET'])
def user_edits():
  if 'username' in session:
    all_edits = db.posts.find({'author': session['username'], 'is_original': False})
    return render_template('user_edits.html', all_edits=all_edits)
  else:
    return redirect(url_for('auth.login'))


def sortFeed(e):
  return e['created_at']