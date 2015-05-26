import datetime
from flask import request, jsonify
from server import app, db
from server.auth import get_or_create
from server.channel import Video, Comment, FeedItem
from server.user import User
from server.util import get_video_url


@app.route('/api/follow', methods=['POST'])
def follow():
    params = request.get_json()
    access_token = params['access_token']
    user_to_follow = params['user_to_follow']
    user = get_or_create(access_token)
    to_follow = User.query.filter(User.id == user_to_follow).one()
    user.following.append(to_follow)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True
    })

@app.route('/api/unfollow', methods=['POST'])
def unfollow():
    params = request.get_json()
    access_token = params['access_token']
    user_to_unfollow = params['user_to_unfollow']
    user = get_or_create(access_token)
    to_unfollow = User.query.filter(User.id == user_to_unfollow).one()
    user.following.remove(to_unfollow)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True
    })

@app.route('/api/comment', methods=['POST'])
def comment():
    params = request.get_json()
    access_token = params['access_token']
    message = params['message']
    video_id = params['video']
    user = get_or_create(access_token)
    video = Video.query.filter_by(id=video_id).first()

    db_comment = Comment(message, user, video)
    video.comments.append(db_comment)
    db.session.add(db_comment)
    db.session.add(user)
    db.session.add(video)
    db.session.commit()  # Needed in order to create an ID for the comment
    create_feed_comment(user, db_comment)
    db.session.commit()

    return jsonify({
        'success': True
    })


def create_feed_like(user, video):
    """
    Adds an item to the users feed
    Does not commit the item to the database
    """
    feed_item = FeedItem(user, 0, video)
    db.session.add(feed_item)


def create_feed_comment(user, comment):
    """
    Adds an item to the users feed
    Does not commit the item to the database
    """
    feed_item = FeedItem(user, 1, comment)
    db.session.add(feed_item)


def simple_user_list(followers, page):
    base_resp = {
        'page': page,
        'total-pages': 1,
        'total-followers': len(followers)
    }

    if page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    follower_list = []
    for follower in followers:
        follower_list.append({
            'id': follower.id,
            'name': follower.name
        })
    return jsonify(dict(base_resp, followers=follower_list))


@app.route('/api/my-followers/')
@app.route('/api/my-followers/<int:page>')
def my_followers(page=1):
    """
    Currently using fake pagination
    """
    user = get_or_create(request.headers['access_token'])
    return simple_user_list(user.followers, page)


@app.route('/api/following/')
@app.route('/api/following/<int:page>')
def following(page):
    """
    Currently using fake pagination
    """
    user = get_or_create(request.headers['access_token'])
    return simple_user_list(user.following, page)

@app.route('/api/toggle-like/<int:video_id>')
def toggle_like(video_id):
    """
    Likes an video. If the the user already likes the video, it reverses the action.
    """
    user = get_or_create(request.headers['access_token'])
    video = Video.query.filter_by(id=video_id).first()

    i_am_liking = False

    for like in video.liking_users:
        if like.id == user.id:
            i_am_liking = True
            break


    if i_am_liking:
        user.liked_videos.remove(video)
    else:
        user.liked_videos.append(video)
        create_feed_like(user, video)
    db.session.commit()

    return jsonify({
        "liking": not i_am_liking
    })

@app.route('/api/likes/<int:video_id>')
def likes(video_id):
    video = Video.query.filter_by(id=video_id).first()
    user = get_or_create(request.headers['access_token'])

    i_am_liking = False

    for like in video.liking_users:
        if like.id == user.id:
            i_am_liking = True
            break

    return jsonify({
        'likes': len(video.liking_users),
        'i-am-liking': i_am_liking
    })

@app.route('/api/comments/<int:video_id>/')
@app.route('/api/comments/<int:video_id>/<int:page>')
def comments(video_id, page=1):
    """
    List of comments, using fake pagination for now
    """
    video = Video.query.filter_by(id=video_id).first()

    base_resp = {
        'page': page,
        'total-pages': 1,
        'total-comments': len(video.comments)
    }

    if page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    comment_list = []
    for comment in video.comments:
        comment_list.append({
            'user': comment.user.name,
            'comment': comment.comment
        })
    return jsonify(dict(base_resp, comments=comment_list))


def create_video_obj(video):
    return {
        'channel-id': video.channel_id,
        'channel-name': video.channel.name,
        'slug': video.slug,
        'url': get_video_url(video),
        'video': video.name,
        'id': video.id
    }


@app.route('/api/feed')
@app.route('/api/feed/<int:page>')
def get_feed(page=1):
    """
    Get all news items in the feed.
    Pagination to come
    """
    user = get_or_create(request.headers['access_token'])
    pagination = FeedItem.query\
        .filter(User.following.any(id=user.id))\
        .order_by(FeedItem.date.desc())\
        .paginate(page, error_out=False)

    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-items': pagination.total
    }

    if len(pagination.items) == 0 and page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    feed_item_list = []
    for feed_item in pagination.items:
        if feed_item.event_type == 0:
            # It's a like
            feed_item_list.append({
                'type': 'like',
                'username': feed_item.user.name,
                'date': feed_item.date.replace(microsecond=0).isoformat('T'),
                'videoInf': create_video_obj(feed_item.like)
            })
        elif feed_item.event_type == 1:
            # It's a comment
            feed_item_list.append({
                'type': 'comment',
                'username': feed_item.user.name,
                'date': feed_item.date.replace(microsecond=0).isoformat('T'),
                'comment': {
                    'text': feed_item.comment.comment,
                    'videoInf': create_video_obj(feed_item.comment.video)
                }
            })

    return jsonify(dict(base_resp, items=feed_item_list))

