from flask import request, jsonify
from server import app, db
import requests
from server.user import User


def get_user_id(access_token):
    resp = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    json = resp.json()
    return json['user_id']


def get_name(access_token):
    resp = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={
        'Authorization': 'Bearer ' + access_token
    })
    return resp.json()['name']


def get_or_create(access_token):
    google_id = get_user_id(access_token)
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        print('Created new user')
        user = User(get_name(access_token), google_id)
        db.session.add(user)
        db.session.commit()

    return user


@app.route('/auth', methods=['POST'])
def login():
    params = request.get_json()
    access_token = params['access_token']
    user = get_or_create(access_token)

    return jsonify({
        'success': True,
        'name': user.name
    })