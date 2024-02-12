from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .models import AudioFile, Test, UserAnswer
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify(message="Welcome to ODEUM"), 200

@main.route('/audiofiles', methods=['GET'])
@login_required
def get_audiofiles():
    audiofiles = AudioFile.query.all()
    audiofiles_data = [{"id": audiofile.id, "song_name": audiofile.song_name} for audiofile in audiofiles]
    return jsonify(audiofiles=audiofiles_data), 200

@main.route('/test', methods=['POST'])
@login_required
def start_test():
    # This could be used to create a new test instance for a user
    new_test = Test(user_id=current_user.id)
    db.session.add(new_test)
    db.session.commit()
    return jsonify(message="Test started", test_id=new_test.id), 201

@main.route('/submit_answers', methods=['POST'])
@login_required
def submit_answers():
    data = request.get_json()
    test_id = data['test_id']
    answers = data['answers']

    for answer in answers:
        new_answer = UserAnswer(
            test_id=test_id,
            audiofile_id=answer['audiofile_id'],
            genre=answer['genre'],
            mood=answer['mood'],
            vocal_timbre=answer['vocal_timbre']
        )
        db.session.add(new_answer)

    db.session.commit()
    return jsonify(message="Answers submitted successfully"), 200

@main.route('/test_results/<int:test_id>', methods=['GET'])
@login_required
def get_test_results(test_id):
    test_answers = UserAnswer.query.filter_by(test_id=test_id).all()
    results = []
    for answer in test_answers:
        audiofile = AudioFile.query.get(answer.audiofile_id)
        results.append({
            "song_name": audiofile.song_name,
            "genre": answer.genre,
            "mood": answer.mood,
            "vocal_timbre": answer.vocal_timbre
        })
    return jsonify(test_results=results), 200
