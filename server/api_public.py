"""
This file contains all requests that are to be used by
the end user. Examples include searching for channels and
videos
"""

from flask import jsonify
from server import app, db
from server.channel import Video, Channel


@app.route('/api/channels/')
@app.route('/api/channels/<int:page>')
def list_channels(page=1):
    pagination = Channel.query.paginate(page, error_out=False)

    # Base response will always be used as the base, even if
    # the request fails
    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-channels': pagination.total
    }

    if len(pagination.items) == 0:
        return jsonify(dict(base_resp, error='Page not found')), 404

    channel_list = []
    for channel in pagination.items:
        channel_list.append({
            'channel': channel.name,
            'slug': channel.slug,
            'url': channel.url
        })
    return jsonify(dict(base_resp, channels=channel_list))

@app.route('/api/videos/')
@app.route('/api/videos/<int:page>')
def list_videos(page=1):
    pagination = Video.query.paginate(page, error_out=False)

    # Base response will always be used as the base, even if
    # the request fails
    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-videos': pagination.total
    }

    if len(pagination.items) == 0:
        return jsonify(dict(base_resp, error='Page not found')), 404

    video_list = []
    for video in pagination.items:
        video_list.append({
            'video': video.name,
            'slug': video.slug,
            'channel-id': video.channel_id,
            'channel-name': video.channel.name
        })
    return jsonify(dict(base_resp, videos=video_list))
