"""
This file contains all API requests that are meant for channel
owners, such as registering channels and adding videos to them
"""

import re
from flask import request, jsonify
from server import app
from server.channel import create_channel, ChannelExistsError, authenticate_channel, post_video, ChannelNotFoundError, \
    IncorrectPasswordError, SlugExistsError
from server.util import invalid_parameter, invalid_request

@app.route('/channel/newvideo', methods=['POST'])
def add_new_video():
    """
    The API for adding a new video to an existing channel

    HTTP POST /channel/newvideo {
        channel-slug: The channel slug, acting as the unique login
        channel-password: The channel password
        video-slug: The slug, should be unique for the channel
        video-name: The video name, used both for searching and display
    }
    """
    params = request.get_json()

    # Parameter validation

    if not params:
        return invalid_request('The request body is not valid JSON')

    # channel-slug: The channel slug, acting as the unique login
    if 'channel-slug' not in params:
        return invalid_parameter('channel-slug', 'Slug is required')

    # channel-password: The channel password
    if 'channel-password' not in params:
        return invalid_parameter('channel-password', 'Password is required')

    # video-slug: The slug, should be unique for the channel.
    # The video slug together with the channel url is enough to find all resources regarding
    # the video, including the description and the video itself.
    if 'video-slug' not in params:
        return invalid_parameter('video-slug', 'A video slug is required')

    # video-name: The video name, used both for searching and display
    if 'video-name' not in params:
        return invalid_parameter('video-name', 'The video name is required')

    try:
        channel_account = authenticate_channel(params['channel-slug'], params['channel-password'])
    except ChannelNotFoundError:
        return invalid_parameter('channel-slug', 'Channel with the provided slug was not found')
    except IncorrectPasswordError:
        return invalid_parameter('channel-password', 'The provided channel password is invalid')

    try:
        post_video(channel_account, params['video-slug'], params['video-name'])
    except SlugExistsError:
        return invalid_parameter('video-slug', 'There\'s already a video with that slug')

    return jsonify({
        'message': 'Video added'
    })



@app.route('/channel/register', methods=['POST'])
def register_channel():
    """
    The API for creating a new channel.

    HTTP POST /channel/register {
        name: Channel display name, max length 80 characters
        slug: Channel slug (url-friendly name), [a-z0-9-], max 80 characters
        url: Remote server url where the channel is hosted, max 256 characters
        password: The password required for modifying the channel in the future
    }
    """
    params = request.get_json()

    # Parameter validation

    if not params:
        return invalid_request('The request body is not valid JSON')

    # Hosted By: The name of the hoster
    if 'hosted-by' not in params:
        return invalid_parameter('hosted-by', 'Hosted by is required')
    if len(params['hosted-by']) > 80:
        return invalid_parameter('hosted-by', 'Hosted by is too long (max 80 chars)')

    # name: The channel name, required. Can contain any letters.
    if 'name' not in params:
        return invalid_parameter('name', 'A channel name is required')

    if len(params['name']) > 80:
        return invalid_parameter('name', 'The name may not be longer than 80 characters')

    # slug: The channel's "slug", the url-friendly version of the name.
    # Will in most cases be a lowercase version of the name.
    if 'slug' not in params:
        return invalid_parameter('slug', 'A slug is required')

    if not re.match('^[a-z0-9-]*$', params['slug']):
        return invalid_parameter('slug', 'The slug may only contain [a-z0-9-]')

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
        create_channel(params['name'], params['slug'], params['url'], params['password'], params['hosted-by'])
    except ChannelExistsError:
        return invalid_parameter('slug', 'The slug is already in use')

    return jsonify({
        'message': 'Channel created'
    })