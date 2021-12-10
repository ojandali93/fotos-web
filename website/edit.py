from flask import Blueprint, render_template, request, flash, redirect, url_for, session, send_file
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import app, db
from bson.objectid import ObjectId
from os import path, mkdir

edit = Blueprint('edit', __name__)

# download photo
@edit.route('/download/<photo_id>', methods=['GET'])
def download_photo(photo_id):
  if 'username' in session:
    current_photo = db.posts.find_one({'_id': ObjectId(photo_id)})
    image_name = current_photo['filename'].replace(' ', '_')
    download_file_name = 'static/' + image_name
    db.users.update_one({ 'username' : session['username']}, {'$push': {'downloads': current_photo}})
    db.users.update_one({ 'username' : session['username']}, {'$inc': {'downloads_count': 1}})
    return send_file(download_file_name, as_attachment=True)
  else:
    return redirect(url_for('auth.login'))

@edit.route('/delete/<photo_id>', methods=['POST'])
def delete_edit(photo_id):
  if 'username' in session:
    current_photo = db.post.find_one({'_id': ObjectId(photo_id)})
    if current_photo:
      db.posts.delete_one({'_id': ObjectId(photo_id)})
      return redirect(url_for('views.user_edits'))
  else:
    return redirect(url_for('auth.login'))

@edit.route('/upload/<original_id>', methods=['GET', 'POST'])
def create_edit(original_id):
  if 'username' in session:
    current_user = db.users.find_one({ 'username' : session['username']})
    if request.method == 'POST':
      data = request.form 
      original = data.get('original')
      # original = origin[:-1]
      original_photo = db.posts.find_one({'_id' : ObjectId(original)})
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
        'is_original': False,
        'original': original_photo,
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
      db.users.update_one({ 'username' : session['username']}, {'$push': {'edit_list': new_post}})
      db.users.update_one({ 'username' : session['username']}, {'$inc': {'edit_count': 1}})
      db.posts.update_one({'_id' : ObjectId(original)}, {'$push': {'edit_list': new_post}})
      db.posts.update_one({'_id' : ObjectId(original)}, {'$inc': {'edits_count': 1}})
      flash('New post was created!', category='success')
      return redirect(url_for('views.user_edits'))
    original_post = db.posts.find_one({'_id' : ObjectId(original_id)})
    return render_template('create_edit.html', original_post=original_post)
  else:
    return redirect(url_for('auth.login'))