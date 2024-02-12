from flask import Blueprint, request, jsonify, send_from_directory
from .models import AudioFile, Test, UserAnswer
from . import db
from werkzeug.utils import secure_filename
import os

test_api = Blueprint('test_api', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@test_api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message="No selected file"), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        new_audiofile = AudioFile(file_path=file_path)
        db.session.add(new_audiofile)
        db.session.commit()
        return jsonify(message="File uploaded successfully", id=new_audiofile.id), 201
    return jsonify(message="Invalid file type"), 400

@test_api.route('/test/submit', methods=['POST'])
def submit_test():
    data = request.get_json()
    test = Test(user_id=data['user_id'])
    db.session.add(test)
    db.session.commit()

    for answer in data['answers']:
        user_answer = UserAnswer(test_id=test.id, audiofile_id=answer['audiofile_id'], rating=answer['rating'])
        db.session.add(user_answer)

    db.session.commit()
    return jsonify(message="Test submitted successfully"), 201
