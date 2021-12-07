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
    image_name = current_photo['image_name'].replace(' ', '_')
    download_file_name = 'static/' + image_name
    return send_file(download_file_name, as_attachment=True)
  else:
    return redirect(url_for('auth.login'))


@post.route('/upload', methods=['GET', 'POST'])
def create_post():
  if 'username' in session:
    current_user = db.users.find_one({ 'username' : session['username']})
    if request.method == 'POST':
      data = request.form 
      photo = request.files['photo']
      print(photo)
      photo.save(path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
      caption = data.get('caption')
      location = data.get('location')
      new_post = {
        'image_name': photo.filename, 
        'caption': caption, 
        'location': location,
        'author': session['username'],
        'is_original': True,
        'original': {},
        'downloaded': [],
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
      current_user['photo_list'].append(new_post)
      current_user['photo_count'] += 1
      flash('New post was created!', category='success')
      return redirect(url_for('post.all_posts'))
    return render_template('create_post.html')
  else:
    return redirect(url_for('auth.login'))