import re
from flask import request, jsonify
from server import app
from server.channel import create_channel
from server.util import invalid_parameter


@app.route('/channel/register', methods=['POST'])
def register_channel():
    """
    The API for creating a new channel.

    HTTP POST /channel/register {
        name: Channel display name, max length 80 characters
        slug: Channel slug (url-friendly name), [a-z-], max 80 characters
        url: Remote server url where the channel is hosted, max 256 characters
        password: The password required for modifying the channel in the future
    }
    """
    params = request.get_json()

    # Parameter validation

    # name: The channel name, required. Can contain any letters.
    if 'name' not in params:
        return invalid_parameter('name', 'A channel name is required')

    if len(params['name']) > 80:
        return invalid_parameter('name', 'The name may not be longer than 80 characters')

    # slug: The channel's "slug", the url-friendly version of the name.
    # Will in most cases be a lowercase version of the name.
    if 'slug' not in params:
        return invalid_parameter('slug', 'A slug is required')

    if not re.match('^[a-z-]*$', params['slug']):
        return invalid_parameter('slug', 'The slug may only contain [a-z-]')

    if len(params['slug']) > 80:
        return invalid_parameter('slug', 'The slug may not be longer than 80 characters')

    # url: The remote url that the channel is hosted on.
    # It could for example be http://channels.opid.io/channel-name
    if 'url' not in params:
        return invalid_parameter('url', 'The remote channel url is required')

    if len(params['url']) > 256:
        return invalid_parameter('url', 'The url may not be longer than 256 characters')

    # password: The password required to modify the channel in the future
    if 'password' not in params:
        return invalid_parameter('password', 'A password is required')

    try:
        create_channel(params['name'], params['slug'], params['url'], params['password'])
    except BlockingIOError:
        pass

    return jsonify({
        'message': 'Channel created'
    })