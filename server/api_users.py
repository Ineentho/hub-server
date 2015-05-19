from flask import request, jsonify
from server import app
from server.auth import get_or_create


@app.route('/follow', methods=['POST'])
def follow():
    params = request.get_json()
    access_token = params['access_token']
    user = get_or_create(access_token)

    return jsonify({
        'success': True,
        'name': user.name
    })