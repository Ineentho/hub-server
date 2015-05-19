from flask import request, jsonify
from server import app, db
from server.auth import get_or_create
from server.user import User


@app.route('/api/follow', methods=['POST'])
def follow():
    params = request.get_json()
    access_token = params['access_token']
    user_to_follow = params['user_to_follow']
    user = get_or_create(access_token)
    print('found user')
    to_follow = User.query.filter(User.id == user_to_follow).one()
    user.following.append(to_follow)
    db.session.add(user)
    db.session.commit()


    return jsonify({
        'success': True,
        'name': user.name
    })