import os
from server import app
from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic.providers import oauth2
from flask import Flask, request, make_response, jsonify


CONFIG = {
    'google': {
        'class_': oauth2.Google,
        'consumer_key': os.environ.get('GOOGLE_CONSUMER_KEY'),
        'consumer_secret': os.environ.get('GOOGLE_CONSUMER_SECRET'),
        'scope': oauth2.Google.user_info_scope,
        },
    }

authomatic = Authomatic(CONFIG, 'is this needed?')

@app.route('/login/<provider>', methods=['GET', 'POST'])
def login(provider):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider)

    if result:
        if result.user:
            # Logged in
            return jsonify({
                'success': True,
                'name': result.user.name
            })

        return jsonify({
            'success': False,
            result: result
        })
    return response