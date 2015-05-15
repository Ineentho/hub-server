from flask import request, jsonify
import httplib2
from oauth2client import client
from server import app
import requests


def get_user(access_token):
    resp = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    json = resp.json()
    return json['user_id']


def get_name(access_token):
    resp = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={
        'Authorization': 'Bearer ' + access_token
    })
    return resp.json()['name']


@app.route('/auth', methods=['POST'])
def login():
    params = request.get_json()
    access_token = params['access_token']
    name = get_name(access_token)

    return jsonify({
        'success': True,
        'name': name
    })