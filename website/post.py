from flask import Blueprint, render_template, request, flash, redirect, url_for, session, send_file
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import app, db
from bson.objectid import ObjectId
from os import path, mkdir

post = Blueprint('post', __name__)

# download photo
@post.route('/download/<photo_id>', methods=['GET'])
def download_photo(photo_id):
  if 'username' in session:
    current_photo = db.posts.find_one({'_id': ObjectId(photo_id)})
    user_by_username = db.users.find_one({'username' : session['username']})
    print(user_by_username)
    image_name = current_photo['filename'].replace(' ', '_')
    download_file_name = 'static/images/' + image_name
    db.users.update({ 'username' : session['username']}, {'$push': {'downloads': current_photo}})
    db.users.update({ 'username' : session['username']}, {'$inc': {'downloads_count': 1}})
    db.posts.update({'_id' : ObjectId(photo_id)}, {'$push': {'downloaded_by': session['username']}})
    return send_file(download_file_name, as_attachment=True)
  else:
    return redirect(url_for('auth.login'))

# @post.route('/like/<photo_id>', methods=['GET'])
# def like_post(photo_id)

@post.route('/delete/<photo_id>', methods=['POST'])
def delete_photo(photo_id):
  if 'username' in session:
    current_photo = db.posts.find_one({'_id': ObjectId(photo_id)})
    if current_photo:
      db.posts.delete_one({'_id': ObjectId(photo_id)})
      return redirect(url_for('views.user_photos'))
  else:
    return redirect(url_for('auth.login'))

@post.route('/upload', methods=['GET', 'POST'])
def create_post():
  if 'username' in session:
    current_user = db.users.find_one({ 'username' : session['username']})
    if request.method == 'POST':
      data = request.form 
      photo = request.files['photo']
      photo.save(path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
      image_name = data.get('image_name')
      caption = data.get('caption')
      location = data.get('location')
      new_post = {
        'filename': photo.filename, 
        'image_name': image_name,
        'caption': caption, 
        'location': location,
        'author': session['username'],
        'is_original': True,
        'original': {},
        'downloaded_by': [],
        'edits': [],
        'likes': [],
        'comments': [],
        'downloaded_count': 0,
        'edits_count': 0,
        'likes_count': 0,
        'comments_count': 0,
        'created_at': datetime.now()
      }
      db.posts.insert_one(new_post)
      db.users.update_one({ 'username' : session['username']}, {'$push': {'photo_list': new_post}})
      db.users.update_one({ 'username' : session['username']}, {'$inc': {'photo_count': 1}})
      flash('New post was created!', category='success')
      return redirect(url_for('views.user_photos'))
    return render_template('create_post.html')
  else:
    return redirect(url_for('auth.login'))