from flask import session, jsonify

from MLLM_L.database import User, UserFavoriteProject


def get_user_favorites_2():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    username = session['username']
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_id = user.id
    favorite_projects = UserFavoriteProject.query.filter_by(user_id=user_id).all()

    favorites_list = [favorite.project_id for favorite in favorite_projects]

    return jsonify({'favorites': favorites_list}), 200