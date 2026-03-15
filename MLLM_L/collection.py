from flask import jsonify, request

from MLLM_L.database import HeritageProject, User, UserFavoriteProject, UserFavoriteWork, Work
from MLLM_L.database_all import db


def get_user_favorites(session):
    # 检查当前用户是否已登录
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    username = session['username']
    print(username)

    # 根据用户名查找对应的用户记录
    user = User.query.filter_by(username=username).first()
    print(user)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 获取用户的id
    user_id = user.id
    print(user_id)

    # 查询当前用户收藏的项目
    favorite_projects = UserFavoriteProject.query.filter_by(user_id=user_id).all()
    print(favorite_projects)

    # 构造收藏项目的返回数据
    favorites_list = []
    for favorite in favorite_projects:
        project_id = favorite.project_id
        # 根据收藏关系中的项目id查询对应的项目信息
        project = HeritageProject.query.get(project_id)
        if project:
            project_data = {
                'id': project.id,
                'category_big': project.category_big,
                'category_small': project.category_small,
                'project_name': project.project_name,
                'specific_number': project.specific_number,
                'description': project.description
            }
            favorites_list.append(project_data)

    # 检查收藏功能是否触发（从请求数据中获取要收藏的项目id）
    data = request.get_json()
    if data and 'project_id' in data:
        project_id = data['project_id']
        print(project_id)

        # 检查是否已经存在相同的收藏关系
        existing_favorite = UserFavoriteProject.query.filter_by(user_id=user_id, project_id=project_id).first()
        print(existing_favorite)

        if not existing_favorite:
            # 创建新的收藏关系记录
            new_favorite = UserFavoriteProject(user_id=user_id, project_id=project_id)
            db.session.add(new_favorite)
            db.session.commit()

            # 添加收藏成功的消息
            favorites_list.append({
                'id': project_id,
                'message': 'Project added to favorites successfully'
            })

    print(favorites_list)
    return jsonify({'favorites': favorites_list}), 200


def get_user_favorites_work(session):
    # 检查当前用户是否已登录
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    username = session['username']
    print(username)

    # 根据用户名查找对应的用户记录
    user = User.query.filter_by(username=username).first()
    print(user)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 获取用户的id
    user_id = user.id
    print(user_id)

    # 查询当前用户收藏的项目
    favorite_projects_work = UserFavoriteWork.query.filter_by(user_id=user_id).all()
    print(favorite_projects_work)

    # 构造收藏项目的返回数据
    favorites_list = []
    for favorite in favorite_projects_work:
        work_id = favorite.work_id
        # 根据收藏关系中的项目id查询对应的项目信息
        work = Work.query.get(work_id)
        if work:
            work_data = {
                'id': work.id,
                'category_big': work.category_big,
                'category_small': work.category_small,
                'work_name': work.work_name,
                'specific_number': work.specific_number,
                'price': work.price
            }
            favorites_list.append(work_data)

    # 检查收藏功能是否触发（从请求数据中获取要收藏的项目id）
    data = request.get_json()
    if data and 'work_id' in data:
        work_id = data['work_id']
        print(work_id)

        # 检查是否已经存在相同的收藏关系
        existing_favorite = UserFavoriteWork.query.filter_by(user_id=user_id, work_id=work_id).first()
        print(existing_favorite)

        if not existing_favorite:
            # 创建新的收藏关系记录
            new_favorite = UserFavoriteWork(user_id=user_id, work_id=work_id)
            db.session.add(new_favorite)
            db.session.commit()

            # 添加收藏成功的消息
            favorites_list.append({
                'id': work_id,
                'message': 'Work added to favorites successfully'
            })

    print(favorites_list)
    return jsonify({'favorites': favorites_list}), 200
